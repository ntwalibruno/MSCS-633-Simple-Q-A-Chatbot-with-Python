# Compatibility patch for ChatterBot with Python 3.11+
import sys

def patch_typing_evaluate():
    """
    Patch the typing module to fix ForwardRef._evaluate compatibility
    """
    try:
        from typing import ForwardRef
        import typing
        
        # Store the original _evaluate method if it exists
        if hasattr(ForwardRef, '_evaluate'):
            original_evaluate = ForwardRef._evaluate
            
            # Create a patched version that handles the missing recursive_guard argument
            def patched_evaluate(self, globalns=None, localns=None, recursive_guard=None):
                if recursive_guard is None:
                    recursive_guard = frozenset()
                return original_evaluate(self, globalns, localns, recursive_guard)
            
            # Apply the patch
            ForwardRef._evaluate = patched_evaluate
            
        return True
    except Exception as e:
        print(f"Failed to patch typing module: {e}")
        return False

# Apply the patch when this module is imported
patch_typing_evaluate()