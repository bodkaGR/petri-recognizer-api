
class XMLUtils:

    @staticmethod
    def get_namespace(root):
        """Extracts namespace if exist"""
        if root.tag.startswith("{"):
            return root.tag[1:].split("}")[0]
        return ""

    @staticmethod
    def find_all(element, tag, ns=""):
        """Find all elements with a given tag (supports optional namespace)"""
        return element.findall(f".//{{{ns}}}{tag}") if ns else element.findall(f".//{tag}")

    @staticmethod
    def find(element, path, ns=""):
        """Find a single sub-element by path"""
        return element.find(f".//{{{ns}}}{path}") if ns else element.find(f".//{path}")