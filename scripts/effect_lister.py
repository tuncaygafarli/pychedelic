from modules.module_manager import ModuleManager

def listEffects(args):
    moduleManager = ModuleManager()

    for effect, functions in moduleManager.effects_functions.items():
        print(f"{effect} - {functions}\n")