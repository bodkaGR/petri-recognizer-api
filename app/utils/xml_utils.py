
class XMLUtils:

    @staticmethod
    def get_namespace(root):
        """Extract namespace URI if present"""
        if root.tag.startswith("{"):
            return root.tag[1:].split("}")[0]
        return ""

    @staticmethod
    def _ns_path(path: str, ns: str) -> str:
        """Add namespace to every segment in the path"""
        if not ns:
            return path
        parts = path.split("/")
        return "/".join(f"{{{ns}}}{p}" for p in parts)

    @staticmethod
    def find_all(element, tag, ns=""):
        """Find all elements with a given tag (supports namespace)"""
        if ns:
            return element.findall(f".//{{{ns}}}{tag}")
        return element.findall(f".//{tag}")

    @staticmethod
    def find(element, path, ns=""):
        """Find a single sub-element by path (namespace-safe)"""
        path_with_ns = XMLUtils._ns_path(path, ns)
        return element.find(path_with_ns)