import magic

images_type = [
    "image/x-icon",
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/bmp",
    "image/webp",
    "image/svg+xml",
    "image/tiff",
    "image/avif",
    "image/heic",
    "image/x-raw",
]

CONTENT_TYPE_PDF = "application/pdf"
CONTENT_TYPE_TXT = "text/plain"
CONTENT_TYPE_CSV = "text/csv"
CONTENT_TYPE_TSV = "text/tab-separated-values"
CONTENT_TYPE_RTF = "application/rtf"
CONTENT_TYPE_ODT = "application/vnd.oasis.opendocument.text"
CONTENT_TYPE_DOC = "application/msword"
CONTENT_TYPE_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

CONTENT_TYPE_XLS = "application/vnd.ms-excel"
CONTENT_TYPE_XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
CONTENT_TYPE_ODS = "application/vnd.oasis.opendocument.spreadsheet"

CONTENT_TYPE_PPT = "application/vnd.ms-powerpoint"
CONTENT_TYPE_PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
CONTENT_TYPE_ODP = "application/vnd.oasis.opendocument.presentation"

CONTENT_TYPE_MP3 = "audio/mpeg"
CONTENT_TYPE_WAV = "audio/wav"
CONTENT_TYPE_OGG = "audio/ogg"
CONTENT_TYPE_AAC = "audio/aac"
CONTENT_TYPE_FLAC = "audio/flac"
CONTENT_TYPE_M4A = "audio/mp4"

CONTENT_TYPE_MP4 = "video/mp4"
CONTENT_TYPE_AVI = "video/x-msvideo"
CONTENT_TYPE_MOV = "video/quicktime"
CONTENT_TYPE_WMV = "video/x-ms-wmv"
CONTENT_TYPE_FLV = "video/x-flv"
CONTENT_TYPE_MKV = "video/x-matroska"
CONTENT_TYPE_WEBM = "video/webm"
CONTENT_TYPE_MPEG = "video/mpeg"

CONTENT_TYPE_ZIP = "application/zip"
CONTENT_TYPE_RAR = "application/vnd.rar"
CONTENT_TYPE_7Z = "application/x-7z-compressed"
CONTENT_TYPE_GZIP = "application/gzip"
CONTENT_TYPE_TAR = "application/x-tar"
CONTENT_TYPE_BZIP2 = "application/x-bzip2"

CONTENT_TYPE_TTF = "font/ttf"
CONTENT_TYPE_OTF = "font/otf"
CONTENT_TYPE_WOFF = "font/woff"
CONTENT_TYPE_WOFF2 = "font/woff2"

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_XML = "application/xml"  
CONTENT_TYPE_YAML = "application/x-yaml"  
CONTENT_TYPE_HTML = "text/html"
CONTENT_TYPE_CSS = "text/css"
CONTENT_TYPE_JS = "application/javascript"  

CONTENT_TYPE_EPUB = "application/epub+zip"
CONTENT_TYPE_CALENDAR = "text/calendar"  
CONTENT_TYPE_PKCS12 = "application/x-pkcs12"  
CONTENT_TYPE_JAR = "application/java-archive"


def get_content_type(file):
    if hasattr(file, "temporary_file_path"):
        content_type = magic.from_file(file.temporary_file_path(), mime=True)
    else:
        content_type = magic.from_buffer(file.read(), mime=True)

    if hasattr(file, "seek") and callable(file.seek):
        file.seek(0)

    return content_type
