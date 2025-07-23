import re
from typing import Optional


def empty_str_to_none(value: str) -> Optional[str]:
    """
    Convierte un string vacío o con solo espacios a None.
    Es un validador 'before' reutilizable para Pydantic.
    """
    if isinstance(value, str) and not value.strip():
        return None
    return value


def create_title_validator(min_length: int = 5):
    """
    Fábrica de validadores para títulos.
    Genera un validador que revisa la longitud mínima y caracteres especiales.
    """

    def validator(value: str) -> str:
        if not isinstance(value, str):
            # No podemos procesar si no es un string
            return value

        cleaned_value = value.lower()

        if len(cleaned_value) < min_length:
            raise ValueError(f"Debe tener al menos {min_length} caracteres.")

        if not re.fullmatch(r"[a-záéíóúñ0-9 ]+", cleaned_value):
            raise ValueError("No puede contener caracteres especiales.")

        return cleaned_value

    return validator
