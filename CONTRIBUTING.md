# Contributing to Purrify

Thank you for your interest in contributing to Purrify! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or later
- Git
- Basic knowledge of Python, system administration, and cross-platform development

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/purrify.git
   cd purrify
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 🏗️ Project Structure

```
purrify/
├── src/purrify/           # Main source code
│   ├── core/             # Core engine and configuration
│   ├── scanners/         # System scanning modules
│   ├── cleaners/         # Cache and file cleaning
│   ├── optimizers/       # Performance optimization
│   ├── ai/              # AI/ML components
│   ├── gui/             # Graphical user interface
│   └── utils/           # Utility functions
├── tests/               # Test suite
├── docs/               # Documentation
├── scripts/            # Build and deployment scripts
└── resources/          # Application resources
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_scanners/
python -m pytest tests/test_cleaners/
python -m pytest tests/test_ai/

# Run with coverage
python -m pytest --cov=src tests/

# Run with verbose output
python -m pytest -v tests/
```

### Writing Tests

- Follow the existing test structure
- Use descriptive test names
- Include both unit and integration tests
- Mock external dependencies
- Test both success and failure scenarios

## 📝 Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

- Line length: 88 characters (Black default)
- Use type hints for all function parameters and return values
- Use docstrings for all public functions and classes
- Follow Google-style docstrings

### Code Formatting

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Check code style with flake8
flake8 src/ tests/
```

### Type Checking

```bash
# Run type checking with mypy
mypy src/
```

## 🔧 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following the style guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No new warnings or errors
- [ ] Cross-platform compatibility verified

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Platform Testing
- [ ] macOS tested
- [ ] Windows tested
- [ ] Linux tested (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues
2. Try the latest version
3. Reproduce the issue
4. Gather system information

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## System Information
- OS: [macOS/Windows/Linux]
- Version: [OS version]
- Python: [Python version]
- Purrify: [Purrify version]

## Additional Information
Logs, screenshots, etc.
```

## 💡 Feature Requests

### Before Requesting

1. Check existing feature requests
2. Consider if it fits the project scope
3. Think about implementation complexity

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why this feature is needed

## Proposed Implementation
How it could be implemented

## Alternatives Considered
Other approaches considered

## Additional Information
Mockups, examples, etc.
```

## 🔒 Security

### Reporting Security Issues

If you discover a security vulnerability, please:

1. **DO NOT** create a public issue
2. Email security@purrify.app
3. Include detailed information about the vulnerability
4. Allow time for assessment and response

### Security Guidelines

- Never commit sensitive information
- Use environment variables for secrets
- Validate all user inputs
- Follow secure coding practices
- Test for common vulnerabilities

## 📚 Documentation

### Documentation Guidelines

- Write clear, concise documentation
- Include examples and use cases
- Keep documentation up to date
- Use consistent formatting
- Include troubleshooting sections

### Documentation Structure

```
docs/
├── user-guide/          # User documentation
├── developer-guide/     # Developer documentation
├── api-reference/       # API documentation
└── tutorials/          # Tutorials and examples
```

## 🏷️ Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## 📄 License

By contributing to Purrify, you agree that your contributions will be licensed under the MIT License.

## 🤝 Community

### Getting Help

- Check the documentation
- Search existing issues
- Join our community discussions
- Ask questions in GitHub Discussions

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and constructive
- Focus on what is best for the community

## 🙏 Acknowledgments

Thank you for contributing to Purrify! Your contributions help make system optimization accessible to everyone.

---

**Happy coding! 🐱✨** 