
# 🤝 Contributing to `gitlab-self-healing-pipeline`

Thank you for showing interest in contributing to this open-source project!  
Your support will help make CI/CD automation smarter, more resilient, and accessible to the entire DevOps community.

---

## 🧱 About the Project

`gitlab-self-healing-pipeline` is a framework that:
- Enables GitLab pipelines to resume from the last successful stage
- Uses shared progress files + a watchdog script
- Supports multi-runner setups and cron-based recovery

---

## 🚀 Getting Started

### Clone the Repo

```bash
git clone https://github.com/gThiru/gitlab-self-healing-pipeline.git
cd gitlab-self-healing-pipeline
```

### Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔧 Ways to Contribute

- 🐛 Report bugs
- ✨ Suggest new features
- 🧪 Add test coverage
- 📚 Improve docs or examples
- 🔧 Propose enhancements or optimizations

---

## ✅ Pull Request Guidelines

1. Fork the repository
2. Create a new feature branch:
   ```bash
   git checkout -b feature/my-enhancement
   ```
3. Make your changes
4. Update docs if applicable
5. Submit a pull request with a clear description

---

## 🐞 Reporting Issues

Please include:
- Expected vs actual behavior
- Logs or screenshots (if applicable)
- OS / GitLab runner / Python version

Use GitHub Issues to submit:
- Bugs
- Ideas
- Questions

---

## 📜 License

By contributing, you agree that your code will be licensed under the MIT License.

---

We're excited to collaborate with contributors from all backgrounds.
Let’s build more resilient pipelines together 💪
