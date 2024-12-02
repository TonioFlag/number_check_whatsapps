# 🟢 Verificador de Números de WhatsApp con Selenium

Este script en Python utiliza **Selenium** para verificar automáticamente si los números de celular especificados en un archivo CSV están registrados en WhatsApp. Está diseñado para usarse tanto en entornos locales (escritorio) como en Google Colab, ofreciendo flexibilidad para distintos usuarios.

---

## 🚀 Características

- **Automatización con Selenium:** Realiza peticiones a WhatsApp Web para verificar números de celular.
- **Multiplataforma:**
  - 🖥️ **Versión para escritorio**: Requiere instalación local de Selenium y Microsoft Edge Driver.
  - 🌐 **Versión en Google Colab**: No requiere instalación de programas.
- **Gestión eficiente de datos:**
  - Entrada: archivo CSV con las columnas `["Móvil", "Está en Whatsapp?", "Fecha"]`.
  - Salida: archivo CSV actualizado con los resultados (`"Sí"`, `"No"`, `"Error"`) y la fecha de consulta.
- **Control de revisiones:** Evita repetir verificaciones recientes (últimos 6 meses) para optimizar el rendimiento.
- **QR para inicio de sesión:** Genera un QR para iniciar sesión en WhatsApp Web, con hasta 5 intentos de reconexión automáticos.

---

## 🗂️ Estructura del Proyecto

```plaintext
📂 VALIDACIONES_WHATSAPP
├── 📂 version_escritorio
│   ├── `verificador_whatsapps.py`
│   ├── `requirements.txt`
│   └── `base.csv`
│
├── 📂 version_google_colab
│   └── `verificador_whatsapps.ipynb`
│
└── `README.md`
```

---

## 🖥️ Requisitos de Sistema

### Para la Versión de Escritorio

1. **Python 3.8+**  
2. **Librerías necesarias:** (ver archivo `requirements.txt`)  
   - Selenium  
   - Pandas
   - qrcode
3. **Microsoft Edge:** Asegúrate de tenerlo actualizado.  
4. **Microsoft Edge WebDriver:** Incluido en el repositorio. Si necesitas actualizarlo, sigue estos pasos:  
   - Descarga la versión más reciente desde [la página oficial de Microsoft](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).  
   - Reemplaza el archivo `msedgedriver.exe` en el directorio.

### Para la Versión de Google Colab

No se requiere instalación previa. El código se ejecuta directamente en Google Colab y genera automáticamente el archivo `base.csv` actualizado para descargar.

---

## 📑 Uso del Script

### Entrada esperada

Un archivo llamado `base.csv` con el siguiente formato:

| Móvil        | Está en Whatsapp? | Fecha       |
|--------------|-------------------|-------------|
| 1 234567890  | Sí                | 2024-05-15  |
| 9876543210   | No                | 2023-10-12  |
| +1029384756  |                   |             |

### Salida generada

El archivo `base.csv` se actualizará con:
- **Estado:** `"Sí"`, `"No"`, o `"Error"`.  
- **Fecha:** Fecha de la consulta más reciente.

---

## ⚙️ Instrucciones de Ejecución

### Ejecución en Escritorio

1. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Coloca tu archivo `base.csv` en la carpeta del proyecto.
3. Ejecuta el script:

   ```bash
   python verificador_whatsapps.py
   ```

### Ejecución en Google Colab
1. Abre el archivo `verificador_whatsapps.ipynb` en Google Colab.
2. Sube tu archivo `base.csv`.
3. Ejecuta el script.
4. Descarga el archivo actualizado.

### Inicio de Sesión
- Genera un código QR para iniciar sesión en WhatsApp Web.
- Realiza hasta 5 intentos de reconexión, con 20 segundos de espera entre cada intento

### Verificación Condicional
- Si el estado de un número es `"Error"` o está vacío, se revisa nuevamente.
- Si la última revisión fue hace más de 6 meses, también se verifica.

### Tiempos de Procesamiento
- **Por número:** Aproximadamente 8 segundos.
- **Reconexión:** Máximo de 5 intentos, con 20 segundos por intento.

---

## 🎉 Contribuciones

Si deseas contribuir al proyecto, no dudes en abrir un *pull request* con tus sugerencias o correcciones. ¡Apreciamos tu ayuda!