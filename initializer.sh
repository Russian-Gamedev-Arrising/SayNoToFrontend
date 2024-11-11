echo "Initialising GitFlow ..." &&
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        apt-get install git-flow
elif [[ "$OSTYPE" == "darwin"* ]]; then
        if ! brew -v | grep -q "Homebrew"
        then /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew -v && brew install git-flow
fi
echo "Initialising pre-commit..." &&
pip install --upgrade pip && 
pip install -r requirements.txt &&
pre-commit install &&
git config --unset-all core.hooksPath &&
echo "Проведите настройку Gitflow: git flow init"