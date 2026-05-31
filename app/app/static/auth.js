document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('[data-login-form]');
    if (!loginForm) {
        return;
    }

    const feedback = document.querySelector('[data-login-feedback]');
    const submitButton = loginForm.querySelector('button[type="submit"]');

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(loginForm);
        const payload = {
            identifier: formData.get('identifier'),
            senha: formData.get('senha')
        };

        feedback.textContent = 'Entrando...';
        feedback.className = 'login-alert info';
        submitButton.disabled = true;

        try {
            const response = await fetch(loginForm.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Nao foi possivel autenticar.');
            }

            window.location.href = '/';
        } catch (error) {
            feedback.textContent = error.message;
            feedback.className = 'login-alert error';
        } finally {
            submitButton.disabled = false;
        }
    });
});
