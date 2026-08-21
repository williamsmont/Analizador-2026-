#!/usr/bin/env python3
"""Genera una cotización de Innovap Solutions SpA en el formato del modelo."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

AZUL = colors.HexColor("#2E6FBA")
AZUL_CLARO = colors.HexColor("#DCEAF7")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Empresa", fontSize=20, leading=24, textColor=AZUL, alignment=TA_CENTER, spaceAfter=6, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Subtitulo", fontSize=10, leading=13, textColor=colors.grey, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name="Titulo", fontSize=12, fontName="Helvetica-Bold", spaceAfter=2))
styles.add(ParagraphStyle(name="Normal9", fontSize=9.5, leading=12))
styles.add(ParagraphStyle(name="NormalCell", fontSize=8.5, leading=11))
styles.add(ParagraphStyle(name="Seccion", fontSize=10, fontName="Helvetica-Bold", textColor=AZUL, spaceBefore=10, spaceAfter=4))

doc = SimpleDocTemplate("cotizacion_2186119cot26.pdf", pagesize=letter,
                         topMargin=1.5*cm, bottomMargin=1.5*cm,
                         leftMargin=2*cm, rightMargin=2*cm)

story = []

# Logo + encabezado
logo = Image("innovap_logo.jpg", width=4.2*cm, height=2.1*cm)
logo.hAlign = "CENTER"
story.append(logo)
story.append(Spacer(1, 14))
story.append(Paragraph("Innovap Solutions SpA", styles["Empresa"]))
story.append(Spacer(1, 4))
story.append(Paragraph("Soluciones Tecnológicas | RUT 78.263.141-1", styles["Subtitulo"]))
story.append(HRFlowable(width="100%", thickness=0.7, color=colors.grey))
story.append(Spacer(1, 10))

story.append(Paragraph("PROPUESTA COMERCIAL N° 2186-119-COT26", styles["Titulo"]))
story.append(Paragraph("21 de Agosto de 2026", styles["Normal9"]))
story.append(Spacer(1, 8))

story.append(Paragraph("Señores", styles["Normal9"]))
story.append(Paragraph(
    "Corporación Administrativa del Poder Judicial &ndash; Zonal Rancagua<br/>"
    "RUT: 60.301.001-9<br/>"
    "Bello Horizonte 845, Torre B, piso 5, comuna de Rancagua, Región del "
    "Libertador General Bernardo O&rsquo;Higgins<br/>Presente.",
    styles["Normal9"]))
story.append(Spacer(1, 10))

story.append(Paragraph("Estimados,", styles["Normal9"]))
story.append(Paragraph(
    "Mediante la presente, enviamos nuestra propuesta comercial por los "
    "siguientes insumos, en respuesta a la Compra Ágil "
    "&ldquo;Adquisición de cámaras web e insumos informáticos&rdquo; "
    "(código 1699-119-COT26):", styles["Normal9"]))
story.append(Spacer(1, 10))

# Datos de items (neto, iva, total) ya calculados para sumar $950.000 total
items = [
    ("1", "Cámara web USB 720p (1280x720), 0,9 Mpx, sensor CMOS, zoom 3x, "
          "interfaz USB-A 2.0, compatible Windows 10/11, PC y notebook, "
          "compatible Skype/Zoom. Marca Philco o equivalente técnico.\n"
          "Cantidad: 10 unidades.", "65.521", "12.449", "77.970"),
    ("2", "Disco duro externo 2TB, formato 2,5\", interfaz USB 3.2 Gen1 "
          "(USB 3.0) hasta 5 Gb/s, copia de seguridad automática y "
          "protección con contraseña. Marca WD (Elements) o equivalente "
          "técnico.\nCantidad: 2 unidades.", "102.353", "19.447", "121.800"),
    ("3", "Escalera articulada multiposición, aluminio, capacidad de carga "
          "150 kg, largo extendido 3,19 m, 12 peldaños, sistema de bloqueo "
          "automático. Marca Karson o equivalente técnico.\n"
          "Cantidad: 1 unidad.", "36.546", "6.944", "43.490"),
    ("4", "UPS interactiva, potencia nominal 600VA / pico 1000VA, batería "
          "12V/9Ah, alarma sonora (batería baja, sobrecarga, modo batería), "
          "indicador LED. Marca Spektra o equivalente técnico.\n"
          "Cantidad: 10 unidades.", "594.235", "112.505", "706.740"),
]

table_data = [["Ítem", "Descripción", "Valor", "IVA", "Total"]]
for it in items:
    table_data.append([
        it[0],
        Paragraph(it[1].replace("\n", "<br/>"), styles["NormalCell"]),
        it[2], it[3], it[4],
    ])

t = Table(table_data, colWidths=[1.2*cm, 8.6*cm, 2.3*cm, 2.1*cm, 2.3*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), AZUL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 9),
    ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
    ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B0C4D8")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [AZUL_CLARO, colors.white]),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 14))

# Resumen de valores
subtotal_neto = 65521 + 102353 + 36546 + 594235
iva_total = 12449 + 19447 + 6944 + 112505
total_propuesta = subtotal_neto + iva_total

resumen_data = [
    ["RESUMEN DE VALORES"],
    [f"Subtotal Neto: $ {subtotal_neto:,}".replace(",", ".")],
    [f"IVA 19%: $ {iva_total:,}".replace(",", ".")],
    [f"TOTAL PROPUESTA: $ {total_propuesta:,}".replace(",", ".")],
]
r = Table(resumen_data, colWidths=[7*cm])
r.setStyle(TableStyle([
    ("BOX", (0, 0), (-1, -1), 1, AZUL),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 3), (-1, 3), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 10),
    ("FONTSIZE", (0, 1), (-1, -1), 9.5),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
resumen_wrapper = Table([[r]], colWidths=[17*cm])
resumen_wrapper.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "RIGHT")]))
story.append(resumen_wrapper)
story.append(Spacer(1, 16))

story.append(Paragraph("CONDICIONES GENERALES", styles["Seccion"]))
story.append(Paragraph(
    "Plazo de entrega: 5 días hábiles, contados desde el envío de la orden "
    "de compra al proveedor, en las dependencias de la Corporación "
    "Administrativa del Poder Judicial, Bello Horizonte 845 Torre B piso 5, "
    "comuna de Rancagua, de lunes a viernes de 8:00 a 15:00 horas.",
    styles["Normal9"]))
story.append(Paragraph(
    "El valor total propuesto incluye todos los costos de despacho, sin "
    "costo adicional para la Corporación.", styles["Normal9"]))
story.append(Paragraph(
    "Todos los productos son nuevos, sin uso, de línea vigente, con "
    "garantía formal mínima de 8 meses y soporte técnico verificable en "
    "Chile.", styles["Normal9"]))
story.append(Spacer(1, 10))

story.append(Paragraph("DATOS PARA TRANSFERENCIA BANCARIA", styles["Seccion"]))
story.append(Paragraph(
    "Innovap Solutions SpA | RUT: 78.263.141-1<br/>"
    "Banco de Chile | Cuenta Vista N° 181925336<br/>"
    "contacto@innovap.cl", styles["Normal9"]))
story.append(Spacer(1, 16))

story.append(Paragraph("Quedamos atentos a sus comentarios.", styles["Normal9"]))
story.append(Spacer(1, 8))
story.append(Paragraph("Saluda atentamente,", styles["Normal9"]))
story.append(Spacer(1, 16))
story.append(Paragraph("<b>Caterin Sonnenburg</b>", styles["Normal9"]))
story.append(Paragraph(
    "Ejecutivo de Cuentas<br/>Innovap Solutions SpA<br/>Móvil: +56 9 62737772",
    styles["Normal9"]))

doc.build(story)
print(f"PDF generado. Subtotal neto: {subtotal_neto} | IVA: {iva_total} | Total: {total_propuesta}")
