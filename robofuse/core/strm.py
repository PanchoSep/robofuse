import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple

from robofuse.utils.logging import logger
from robofuse.utils.parser import MetadataParser


class StrmFile:
    """Class for handling .strm files."""
    
    def __init__(self, output_dir: str, use_ptt_parser: bool = True):
        self.output_dir = Path(output_dir)
        self._ensure_output_dir()
        self.use_ptt_parser = use_ptt_parser
        self.metadata_parser = MetadataParser(enabled=use_ptt_parser)
        self.paths_cache_file = self.output_dir / "processed_paths.json"
        
    
    def _ensure_output_dir(self):
        """Ensure the output directory exists."""
        if not self.output_dir.exists():
            logger.info(f"Creating output directory: {self.output_dir}")
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize a filename to be safe for the filesystem."""
        # Replace illegal characters
        sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
        # Replace multiple spaces with a single space
        sanitized = re.sub(r'\s+', ' ', sanitized)
        # Trim leading/trailing spaces
        sanitized = sanitized.strip()
        # Ensure filename isn't too long
        if len(sanitized) > 240:
            sanitized = sanitized[:240]
        
        return sanitized
    
    def create_or_update_strm(
        self,
        download_url: str,
        filename: str,
        torrent_name: str,
        dry_run: bool = False,
        download_id: Optional[str] = None,
        torrent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        if self.use_ptt_parser:
            metadata = self.metadata_parser.parse(filename)
            logger.verbose(f"Metadata for {filename}: {metadata}")
    
            folder_parts = self.metadata_parser.generate_folder_structure(metadata, torrent_id)
            base_folder_path = self.output_dir
            for part in folder_parts:
                base_folder_path = base_folder_path / self._sanitize_filename(part)
    
            base_filename = self.metadata_parser.generate_filename(metadata)
            safe_filename = self._sanitize_filename(base_filename)
        else:
            base_folder_path = self.output_dir / self._sanitize_filename(torrent_name)
            safe_filename = self._sanitize_filename(filename)
    
        if not safe_filename.lower().endswith('.strm'):
            strm_filename = f"{safe_filename}.strm"
        else:
            strm_filename = safe_filename
    
        self.paths_cache = self._load_paths_cache()
    
        folder_path = base_folder_path
        relative_folder = os.path.relpath(folder_path, self.output_dir)
    
        if torrent_id:
            self.paths_cache.setdefault(torrent_id, [])
            existing_folders = self.paths_cache[torrent_id]
    
            matched_existing = None
            for existing in existing_folders:
                existing_path = self.output_dir / existing
                if existing_path.exists():
                    potential_path = existing_path / strm_filename
                    if potential_path.exists():
                        matched_existing = existing
                        break
    
            if matched_existing:
                folder_path = self.output_dir / matched_existing
                relative_folder = matched_existing
            else:
                # Si ya existe la carpeta base en processed_paths, evitar duplicar y anidar infinitamente
                if relative_folder in existing_folders:
                    folder_path = folder_path / safe_filename
                    relative_folder = os.path.relpath(folder_path, self.output_dir)
    
                if relative_folder not in self.paths_cache[torrent_id]:
                    self.paths_cache[torrent_id].append(relative_folder)
                    self._save_paths_cache()
                    logger.verbose(f"💾 Agregado a processed_paths.json: {torrent_id} → {relative_folder}")
    
        strm_path = folder_path / strm_filename
        is_update = strm_path.exists()
    
        current_url = None
        if is_update:
            try:
                with open(strm_path, 'r') as f:
                    current_url = f.read().strip()
            except Exception as e:
                logger.warning(f"Failed to read existing STRM file: {str(e)}")

        proxy_base_url = "http://127.0.0.1:5000/stream?link="
        proxied_url = f"{proxy_base_url}{download_url}"
    
        if is_update and current_url == proxied_url:
            logger.verbose(f"STRM file already exists with current URL: {strm_path}")
            return {
                "status": "skipped",
                "path": str(strm_path),
                "reason": "file exists with same URL",
                "is_update": False
            }
    
        if dry_run:
            action = "Would update" if is_update else "Would create"
            logger.info(f"{action} STRM file: {strm_path}")
            return {
                "status": "dry_run",
                "path": str(strm_path),
                "action": "update" if is_update else "create",
                "is_update": is_update
            }
    
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
    
        try:
            with open(strm_path, 'w') as f:
                f.write(proxied_url)
    
            action = "Updated" if is_update else "Created"
            logger.success(f"{action} STRM file: {strm_path}")
    
            return {
                "status": "success",
                "path": str(strm_path),
                "action": "update" if is_update else "create",
                "is_update": is_update
            }
        except Exception as e:
            logger.error(f"Failed to write STRM file: {str(e)}")
            return {
                "status": "error",
                "path": str(strm_path),
                "error": str(e)
            }

    
    def delete_strm(self, strm_path: str) -> Dict[str, Any]:
        """Delete a .strm file."""
        path = Path(strm_path)
        
        if not path.exists():
            logger.warning(f"STRM file does not exist: {path}")
            return {
                "status": "error",
                "path": str(path),
                "error": "File does not exist"
            }
        
        try:
            path.unlink()
            logger.success(f"Deleted STRM file: {path}")
            
            # Remove empty parent directory if it's now empty
            parent = path.parent
            if parent.exists() and not any(parent.iterdir()):
                parent.rmdir()
                logger.info(f"Removed empty directory: {parent}")
            
            return {
                "status": "success",
                "path": str(path)
            }
        except Exception as e:
            logger.error(f"Failed to delete STRM file: {str(e)}")
            return {
                "status": "error",
                "path": str(path),
                "error": str(e)
            }
    
    def find_existing_strm_files(self) -> List[Dict[str, Any]]:
        """Find all existing .strm files in the output directory."""
        logger.info(f"Scanning for existing STRM files in {self.output_dir}")
        
        strm_files = []
        
        # Walk through the output directory
        for root, _, files in os.walk(self.output_dir):
            for file in files:
                if file.lower().endswith('.strm'):
                    strm_path = os.path.join(root, file)
                    
                    # Read the URL from the STRM file
                    try:
                        with open(strm_path, 'r') as f:
                            url = f.read().strip()
                        
                        # Extract relative path from output_dir
                        rel_path = os.path.relpath(strm_path, self.output_dir)
                        
                        # Get parts of the path for organized content
                        path_parts = Path(rel_path).parts
                        
                        file_info = {
                            "path": strm_path,
                            "url": url,
                            "filename": os.path.basename(strm_path)
                        }
                        
                        # Add path parts info (useful for organized content)
                        if len(path_parts) >= 2:
                            file_info["parent_folder"] = path_parts[0]
                            if len(path_parts) >= 3 and "season" in path_parts[1].lower():
                                file_info["season_folder"] = path_parts[1]
                        
                        # Add metadata from the filename
                        if self.use_ptt_parser:
                            try:
                                file_metadata = self.metadata_parser.parse(os.path.basename(strm_path))
                                file_info["metadata"] = file_metadata
                            except Exception as e:
                                logger.debug(f"Failed to parse metadata for {strm_path}: {str(e)}")
                        
                        strm_files.append(file_info)
                    except Exception as e:
                        logger.warning(f"Failed to read STRM file {strm_path}: {str(e)}")
        
        logger.info(f"Found {len(strm_files)} existing STRM files")
        return strm_files 

    def _load_paths_cache(self) -> Dict[str, str]:
        if self.paths_cache_file.exists():
            try:
                with open(self.paths_cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"⚠️ Error cargando processed_paths.json: {e}")
        return {}

    def _save_paths_cache(self):
        try:
            with open(self.paths_cache_file, 'w') as f:
                json.dump(self.paths_cache, f, indent=2)
        except Exception as e:
            logger.warning(f"⚠️ Error guardando processed_paths.json: {e}")
