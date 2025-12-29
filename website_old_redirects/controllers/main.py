from odoo import http
from odoo.http import request
import os
import csv
import logging

_logger = logging.getLogger(__name__)

IGNORED_EXTENSIONS = (
    '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.zip', '.rar', '.mp4', '.webm', '.js', '.css'
)

def load_redirects():
    """Charge les anciennes URLs depuis le fichier CSV (nettoyage inclus)"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.abspath(os.path.join(base_path, '..', 'data', 'urls.csv'))

    urls = set()
    try:
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                url = row[0].strip()

                # On ignore les fichiers statiques
                if not url or any(url.lower().endswith(ext) for ext in IGNORED_EXTENSIONS):
                    continue

                # Supprime le domaine si présent
                domain = 'https://www.mobilitix.fr'
                if url.startswith(domain):
                    url = url[len(domain):]

                # Force le / initial
                if url and not url.startswith('/'):
                    url = '/' + url

                urls.add(url)

    except Exception as e:
        _logger.error(f"[REDIRECT] Erreur lecture fichier URLs: {e}")
    return urls

OLD_URLS = load_redirects()

class RedirectController(http.Controller):

    @http.route('/<path:path>', type='http', auth='public', website=True)
    def catch_all_redirect(self, path, **kwargs):
        full_path = '/' + path
        if full_path in OLD_URLS:
            _logger.info(f"[REDIRECT] {full_path} → /")
            return request.redirect('/', code=301)
        return request.not_found()
