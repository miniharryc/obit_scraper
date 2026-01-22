"""
Main module for the Python workspace.
"""


def hello_world(name: str = "World") -> str:
    """
    Return a greeting message.
    
    Args:
        name: The name to greet (default: "World")
    
    Returns:
        A greeting message string
    """
    return f"Hello, {name}!"


def main() -> None:
    """Main entry point for the application."""
    print(hello_world("Python Workspace"))


if __name__ == "__main__":
    main()
