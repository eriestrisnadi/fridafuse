from pathlib import Path

from hatchling.metadata.plugin.interface import MetadataHookInterface


class AboutMetadataHook(MetadataHookInterface):
    def update(self, metadata):
        about_file = Path(self.root) / 'src' / 'fridafuse' / '__about__.py'

        about = {}
        if about_file.is_file():
            with about_file.open(encoding='utf-8') as file:
                exec(file.read(), about)

        about.get('__license__').__delitem__('file')

        metadata['version'] = about.get('__version__', '0.0.0')
        metadata['description'] = about.get('__description__')
        metadata['readme'] = about.get('__readme__')
        metadata['license'] = about.get('__license__')
        metadata['urls'] = about.get('__project_urls__')
        metadata['authors'] = about.get('__authors__')
