docker compose run --rm backend sh -c "python manage.py collectstatic --noinput && \
                                   python manage.py makemigrations && \
                                   python manage.py migrate && \
                                   python manage.py test --parallel"

if [ $? -eq 0 ]; then
    echo "All tests passed"
    git push origin
    if [ $? -eq 0 ]; then
        echo "Synced with github"
    else
        echo "***Changes not pushed to remote***"
    fi
else
    echo "***Tests failed***"
fi
