document.addEventListener('DOMContentLoaded', () => {
    const list = document.getElementById('client-list');
    const search = document.getElementById('client-search');

    const renderClients = (clients) => {
        if (!clients.length) {
            list.innerHTML = '<p class="empty-message">Nenhum cliente encontrado.</p>';
            return;
        }

        list.innerHTML = clients.map((cliente) => `
            <article class="client-card">
                <div class="client-avatar">
                    <img src="/static/icones/Login.png" alt="Cliente">
                </div>
                <div class="client-info">
                    <strong>${cliente.nome || ''} ${cliente.sobrenome || ''}</strong>
                    <span>Usuario: ${cliente.username || '-'}</span>
                    <span>Email: ${cliente.email || '-'}</span>
                    <span>CPF: ${cliente.cpf || '-'}</span>
                    <span>Telefone: ${cliente.telefone || '-'}</span>
                </div>
            </article>
        `).join('');
    };

    const loadClients = async () => {
        const response = await fetch('/api/users', { headers: { Accept: 'application/json' } });
        if (!response.ok) {
            throw new Error('Nao foi possivel carregar os clientes.');
        }

        return response.json();
    };

    const refresh = async () => {
        try {
            const clients = await loadClients();
            const term = search.value.trim().toLowerCase();
            const filtered = clients.filter((cliente) => {
                const searchable = [cliente.nome, cliente.sobrenome, cliente.username, cliente.email, cliente.cpf]
                    .filter(Boolean)
                    .join(' ')
                    .toLowerCase();
                return !term || searchable.includes(term);
            });
            renderClients(filtered);
        } catch (error) {
            list.innerHTML = `<p class="empty-message">${error.message}</p>`;
        }
    };

    search.addEventListener('input', refresh);
    refresh();
});
