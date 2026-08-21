# Plantilla de Cotización — Innovap Solutions SpA

Plantilla base para generar propuestas comerciales / cotizaciones de Innovap
para postular a procesos de Compra Ágil en Mercado Público. Extraída del
modelo real `cotizacion_modelo_innovap.pdf` (Propuesta Comercial N°
2186-281-COT26, 07-ago-2026) guardado en esta misma carpeta.

## Datos fijos de la empresa (no cambian entre cotizaciones)

- **Razón social:** Innovap Solutions SpA
- **Giro:** Soluciones Tecnológicas
- **RUT:** 78.263.141-1
- **Correo:** contacto@innovap.cl
- **Banco:** Banco de Chile
- **Cuenta:** Cuenta Vista N° 181925336
- **Ejecutivo de cuentas:** Caterin Sonnenburg
- **Móvil:** +56 9 62737772
- **Logo:** Innovap Electronics (ver PDF modelo)

## Numeración de propuesta

Formato observado: `N°-N-COT-AA` — coincide con el código externo de la
Compra Ágil en Mercado Público (ej. código ChileCompra `2186-281-COT26` →
Propuesta Comercial N° 2186-281-COT26). **Usar el mismo código de la Compra
Ágil como número de propuesta**, para trazabilidad directa.

## Campos variables por cotización

| Campo | Fuente |
|---|---|
| N° de propuesta | `codigo` de la Compra Ágil (API ChileCompra) |
| Fecha | Fecha de emisión de la cotización |
| Organismo destinatario (nombre) | `institucion.organismo_comprador` |
| RUT organismo | `institucion.rut` |
| Dirección | `entrega.direccion_entrega` |
| Ítems (descripción, valor neto, IVA, total) | Estudio de mercado por producto/servicio |
| Plazo de ejecución/entrega | `entrega.plazo_entrega_dias` (respetar como máximo, no ofrecer más) |
| Exclusiones / condiciones especiales | Según lo que aplique al rubro (ver nota) |

## Estructura de la tabla de ítems

| Ítem | Descripción | Valor (neto) | IVA (19%) | Total |
|---|---|---|---|---|
| 1 | [descripción detallada del producto/servicio, marca/modelo si aplica] | [neto] | [neto×0.19] | [neto×1.19] |
| ... | | | | |

**Resumen de valores** (recuadro destacado al final de la tabla):
- Subtotal Neto: $ [suma de columna Valor]
- IVA 19%: $ [suma de columna IVA]
- TOTAL PROPUESTA: $ [suma de columna Total]

> Los precios de mercado que investigo (retail) normalmente vienen con IVA
> incluido. Para llenar esta plantilla hay que **desglosar**: Neto = Total
> retail ÷ 1.19, IVA = Neto × 0.19. La plantilla de Innovap cotiza en Neto +
> IVA separado, no en "total con IVA incluido" como pide el ToR de algunas
> Compras Ágiles — verificar caso a caso cuál formato exige el organismo y
> ajustar (algunos piden expresamente "valores totales incluido el IVA").

## Condiciones generales (ajustar según el caso)

- Plazo estimado de ejecución/entrega: **[igual o menor al exigido en el ToR]**
- Notas de exclusión relevantes (ej. "No incluye reemplazo de repuestos, se
  cotizan por separado si corresponde") — incluir si aplica al tipo de
  servicio/producto.

## Cierre

- "Quedamos atentos a sus comentarios."
- "Saluda atentamente,"
- Firma: Caterin Sonnenburg, Ejecutivo de Cuentas, Innovap Solutions SpA,
  Móvil: +56 9 62737772

---

## Cómo la voy a usar de ahora en adelante

Para cada Compra Ágil que estudiemos y decidan postular, con esta plantilla
genero una cotización en el mismo formato/tono que el modelo real
(`cotizacion_modelo_innovap.pdf`), rellenando:
1. N° de propuesta = código de la Compra Ágil.
2. Datos del organismo comprador (de la API).
3. Ítems con precios de mi estudio de mercado + margen acordado.
4. Condiciones de entrega según el ToR del proceso.

Se las entrego en el chat como tabla lista para copiar/formatear, o como
archivo (PDF/Word) si lo piden, para que ustedes la suban a la plataforma de
Mercado Público.
