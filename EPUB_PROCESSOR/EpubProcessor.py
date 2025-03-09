import zipfile
from lxml import etree
import os

# always use '/' as a delimeter for file paths
class EpubProcessor:
    def __init__(self, epub_path):
        self.epub_path = epub_path
        self.name = epub_path.split("/")[-1].split(".")[0]
        self.zipfile = []
        
    def _extract_epub_contents(self,epub):
        contents = epub.namelist()
        ncx_names = []
        opf_names = []
        for item in contents:
            extension = item.split('.')[-1].lower()
            if extension == 'ncx':
                ncx_names.append(item)
            if extension == 'opf':
                opf_names.append(item)
        flag = False
        for ncx in ncx_names:
            if 'standard' in ncx:
                ncx_name = ncx
                flag = True
        if not flag:
            ncx_name = ncx_names[0]
        flag = False
        for opf in opf_names:
            if 'standard' in opf:
                opf_name = opf
                flag = True
        if not flag:
            opf_name = opf_names[0]
        page_names = []
        with epub.open(opf_name) as opf:
            opf_content = opf.read()
            opf_tree = etree.fromstring(opf_content)
            namespace = {'dc': 'http://purl.org/dc/elements/1.1/', 'opf': 'http://www.idpf.org/2007/opf'}
            manifest = opf_tree.find('opf:manifest', namespaces=namespace)
            for item in manifest.findall('opf:item[@media-type="image/jpeg"]', namespaces=namespace):
                page_names.append(os.path.join(os.path.dirname(opf_name), item.get('href').replace('/', os.sep)).replace(os.sep, '/'))
            for item in manifest.findall('opf:item[@media-type="image/png"]', namespaces=namespace):
                page_names.append(os.path.join(os.path.dirname(opf_name), item.get('href').replace('/', os.sep)).replace(os.sep, '/'))
        page_items = []
        for page_name in page_names:
            page_items.append(epub.open(page_name))
        return page_names, page_items, ncx_name, opf_name
    
    def convert(self):
        with zipfile.ZipFile(self.epub_path) as epub:
            page_data = self._extract_epub_contents(epub)

        self.zipfiles = page_data[1]

    def saveAsImg(self):
        for i,file in enumerate(self.zipfiles):
            directory = f"PREPROCESSED/{self.name}/PAGE{i+1}"
            os.makedirs(directory,exist_ok=True)

            with open(f"{directory}/Page.jpg", "wb") as output_file:
                output_file.write(file.read())  # Read and save the image data
        
        
# epub_processor = EpubProcessor("EPUB/Jip&Janneke.epub")
# epub_processor.convert()
# epub_processor.saveAsImg()