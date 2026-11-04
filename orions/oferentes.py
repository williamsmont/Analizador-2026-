"""Orions: consulta si una Compra Ágil (COT) tiene oferentes.

Usa la API v2 de Compra Ágil de Mercado Público:
    GET https://api2.mercadopublico.cl/v2/compra-agil/{codigo}
    Cabecera: ticket: <TICKET>   (el mismo ticket de la API v1)

El detalle trae `proveedores_cotizando[]`, que viene vacío si nadie ha cotizado.

Uso rápido:
    export MERCADOPUBLICO_TICKET="tu-ticket"
    python3 -m orions.oferentes 557639-3609-COT26
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field

BASE_URL = "https://api2.mercadopublico.cl/v2/compra-agil"
USER_AGENT = "OrionsBot/1.0 (Innovap)"
COT_RE = re.compile(r"\b\d{3,7}-\d{1,6}-COT\d{2}\b", re.IGNORECASE)


class OrionsError(Exception):
    """Error que se puede mostrar tal cual al usuario del bot."""


@dataclass
class ResultadoOferentes:
    codigo: str
    nombre: str = ""
    organismo: str = ""
    estado: str = ""
    fecha_cierre: str = ""
    proveedores: list[str] = field(default_factory=list)
    campo_presente: bool = True  # False si la API no trajo `proveedores_cotizando`

    @property
    def cantidad(self) -> int:
        return len(self.proveedores)

    @property
    def tiene_oferentes(self) -> bool | None:
        if not self.campo_presente:
            return None
        return self.cantidad > 0


def extraer_codigos(texto: str) -> list[str]:
    """Devuelve los códigos COT que aparecen en un mensaje, en mayúsculas y sin repetir."""
    vistos: list[str] = []
    for c in COT_RE.findall(texto or ""):
        c = c.upper()
        if c not in vistos:
            vistos.append(c)
    return vistos


def _get_json(url: str, ticket: str, intentos: int = 3) -> dict:
    req = urllib.request.Request(
        url, headers={"ticket": ticket, "User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    ultimo: Exception | None = None
    for i in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise OrionsError("El ticket de Mercado Público no es válido.") from e
            if e.code in (400, 404):
                raise OrionsError("No encontré esa Compra Ágil. Revisa el código.") from e
            ultimo = e
            if e.code not in (429, 500, 502, 503, 504):
                break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            ultimo = e
        time.sleep(1.5 * (i + 1))  # la API tolera ~1 consulta por segundo
    raise OrionsError(f"Mercado Público no respondió ({ultimo}). Intenta de nuevo en un rato.")


def _nombre_proveedor(p) -> str:
    if isinstance(p, str):
        return p
    if isinstance(p, dict):
        for k in ("nombre", "razon_social", "nombre_proveedor", "proveedor", "rut"):
            v = p.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
            if isinstance(v, dict):
                return _nombre_proveedor(v)
    return "Proveedor sin nombre"


def _primero(d: dict, *claves: str) -> str:
    for k in claves:
        v = d.get(k)
        if v not in (None, ""):
            return str(v)
    return ""


def interpretar(codigo: str, data: dict) -> ResultadoOferentes:
    """Convierte la respuesta de la API en un ResultadoOferentes."""
    d = data.get("payload", data) if isinstance(data, dict) else {}
    if isinstance(d, list):
        d = d[0] if d else {}
    inst = d.get("institucion") or {}
    presente = "proveedores_cotizando" in d
    provs = d.get("proveedores_cotizando") or []
    return ResultadoOferentes(
        codigo=codigo,
        nombre=_primero(d, "nombre", "titulo"),
        organismo=_primero(inst, "organismo_comprador", "unidad_compra"),
        estado=_primero(d, "estado", "estado_compra"),
        fecha_cierre=_primero(d, "fecha_cierre", "fecha_cierre_cotizacion"),
        proveedores=[_nombre_proveedor(p) for p in provs],
        campo_presente=presente,
    )


def consultar_oferentes(codigo: str, ticket: str | None = None) -> ResultadoOferentes:
    ticket = ticket or os.environ.get("MERCADOPUBLICO_TICKET")
    if not ticket:
        raise OrionsError("Falta configurar MERCADOPUBLICO_TICKET.")
    codigo = codigo.strip().upper()
    data = _get_json(f"{BASE_URL}/{codigo}", ticket)
    return interpretar(codigo, data)


def formatear_mensaje(r: ResultadoOferentes, max_nombres: int = 10) -> str:
    """Texto listo para responder en Telegram."""
    lineas = [f"📋 {r.nombre or r.codigo}"]
    if r.organismo:
        lineas.append(f"🏢 {r.organismo}")
    if r.estado:
        lineas.append(f"📌 Estado: {r.estado}")
    if r.fecha_cierre:
        lineas.append(f"📅 Cierra: {r.fecha_cierre}")
    lineas.append(f"🎫 {r.codigo}")
    lineas.append("")
    if r.tiene_oferentes is None:
        lineas.append("❔ Mercado Público no informó los oferentes de esta compra.")
    elif r.tiene_oferentes:
        s = "es" if r.cantidad != 1 else ""
        lineas.append(f"🟠 SÍ tiene oferentes: {r.cantidad} proveedor{s} cotizando")
        for n in r.proveedores[:max_nombres]:
            lineas.append(f"• {n}")
        if r.cantidad > max_nombres:
            lineas.append(f"• … y {r.cantidad - max_nombres} más")
    else:
        lineas.append("🟢 NO tiene oferentes todavía: nadie ha cotizado")
    lineas.append(
        f"🔗 https://buscador.mercadopublico.cl/ficha?code={r.codigo}"
    )
    return "\n".join(lineas)


def responder(texto: str, ticket: str | None = None) -> str | None:
    """Punto de entrada para el bot: si el mensaje trae códigos COT, devuelve la respuesta.

    Devuelve None si el mensaje no contiene ningún código COT.
    """
    codigos = extraer_codigos(texto)
    if not codigos:
        return None
    partes = []
    for i, c in enumerate(codigos[:5]):
        if i:
            time.sleep(1.1)
        try:
            partes.append(formatear_mensaje(consultar_oferentes(c, ticket)))
        except OrionsError as e:
            partes.append(f"⚠️ {c}: {e}")
    return "\n\n━━━━━━━━\n\n".join(partes)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 -m orions.oferentes <CODIGO-COT>")
    print(responder(" ".join(sys.argv[1:])) or "No encontré ningún código COT.")
