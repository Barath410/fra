from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore",
  )

  app_env: Literal["development", "staging", "production"] = "development"
  api_v1_prefix: str = "/api/v1"
  database_url: str = Field(
    default="mysql+pymysql://root:Lakpra849%40@localhost:3306/vanaadhikar?charset=utf8mb4"
  )
  upload_dir: Path = Path("uploads")
  enable_translation: bool = True
  max_upload_mb: int = 25
  rule_based_recog_dir: Path = Path("../rule_based_recog")
  ocr_language_hint: str = "eng+hin"
  storage_public_base: str = "/uploads"
  google_client_id: str = ""
  google_client_secret: str = ""
  google_redirect_uri: str = "http://localhost:8000/api/v1/auth/google/callback"
  jwt_secret_key: str = "change-me"
  jwt_algorithm: str = "RS256"
  jwt_private_key_path: Path = Field(default=Path(__file__).resolve().parent / "keys" / "jwt_private.pem")
  jwt_public_key_path: Path = Field(default=Path(__file__).resolve().parent / "keys" / "jwt_public.pem")
  frontend_base_url: str = "http://localhost:3000"

  @property
  def sql_alchemy_database_uri(self) -> str:
    return str(self.database_url)

  @property
  def SQLALCHEMY_DATABASE_URI(self) -> str:  # pragma: no cover - backward compat
    return self.sql_alchemy_database_uri

  @property
  def uploads_path(self) -> Path:
    path = Path.cwd() / self.upload_dir
    path.mkdir(parents=True, exist_ok=True)
    return path

  def _load_key(self, key_path: Path) -> str:
    candidate = key_path
    if not candidate.is_absolute():
      candidate = Path.cwd() / key_path
    if not candidate.exists():
      raise FileNotFoundError(f"JWT key not found: {candidate}")
    return candidate.read_text()

  @property
  def jwt_private_key(self) -> str:
    if self.jwt_algorithm.startswith("HS"):
      return self.jwt_secret_key
    return self._load_key(self.jwt_private_key_path)

  @property
  def jwt_public_key(self) -> str:
    if self.jwt_algorithm.startswith("HS"):
      return self.jwt_secret_key
    return self._load_key(self.jwt_public_key_path)

  @property
  def rule_based_script(self) -> Path:
    return self.rule_based_recog_dir / "pipeline_ocr_extract_translate.py"


@lru_cache
def get_settings() -> Settings:
  return Settings()  # type: ignore[arg-type]


settings = get_settings()
