"""
Architype api functions as a mixin
"""
from jaseci.actor.architype import architype
from jaseci.actor.sentinel import sentinel
from jaseci.utils.utils import b64decode_str


class architype_api():
    """
    Architype APIs
    """

    def api_architype_register(self, snt: sentinel = None,
                               code: str = '', encoded: bool = False):
        """
        Create blank or code loaded architype and return object
        """
        if (encoded):
            code = b64decode_str(code)
        arch = snt.register_architype(code)
        if(arch):
            self.extract_arch_aliases(snt, arch)
            return arch.serialize()
        else:
            return [f'Architype not created, invalid code!']

    def api_architype_get(self, arch: architype, mode: str = 'default',
                          detailed: bool = False):
        """
        Get an architype rendered with specific mode
        Valid modes: {default, code, ir, }
        """
        if(mode == 'code'):
            return arch._jac_ast.get_text()
        elif(mode == 'ir'):
            return arch.ir_dict()
        else:
            return arch.serialize(detailed=detailed)

    def api_architype_set(self, arch: architype, code: str,
                          mode: str = 'default'):
        """
        Set code/ir for a architype
        Valid modes: {code, ir, }
        """
        if(mode == 'code' or mode == 'default'):
            arch.register(code)
        elif(mode == 'ir'):
            arch.apply_ir(code)
        else:
            return [f'Invalid mode to set {arch}']
        if(arch.is_active):
            return [f'{arch} registered and active!']
        else:
            return [f'{arch} code issues encountered!']

    def api_architype_list(self, snt: sentinel = None, detailed: bool = False):
        """
        List architypes known to sentinel
        """
        archs = []
        for i in snt.arch_ids.obj_list():
            archs.append(i.serialize(detailed=detailed))
        return archs

    def api_architype_delete(self, arch: architype, snt: sentinel = None):
        """
        Permanently delete sentinel with given id
        """
        self.remove_arch_aliases(snt, arch)
        archid = arch.id
        snt.arch_ids.destroy_obj(arch)
        return [f'Architype {archid} successfully deleted']
