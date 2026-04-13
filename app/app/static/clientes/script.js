$(document).ready(function () {

    // ── Inicializa o DataTable ──────────────────────────────────────────────
    const tabela = $('#tabelaclientes').DataTable({
        lengthChange: false,
        ajax: {
            url: '/cliente/',
            type: 'GET',
            dataSrc: 'clientes'
        },
        columns: [
            { data: 'IDCliente',  visible: false },
            { data: 'Nome' },
            { data: 'CPF' },
            { data: 'Telefone', defaultContent: '-' },
            { data: 'Email',    defaultContent: '-' },
            {
                data: null,
                orderable: false,
                render: function (data) {
                    return `
                        <button class="btn btn-sm btn-warning btn-editar"
                                data-id="${data.IDCliente}"
                                data-nome="${data.Nome}"
                                data-cpf="${data.CPF}"
                                data-telefone="${data.Telefone ?? ''}"
                                data-email="${data.Email ?? ''}">
                            Editar
                        </button>
                        <button class="btn btn-sm btn-danger btn-deletar"
                                data-id="${data.IDCliente}">
                            Excluir
                        </button>`;
                }
            }
        ],
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.0.8/i18n/pt-BR.json'
        }
    });

        document.getElementById("linhas").addEventListener("change", function () {
        tabela.page.len(this.value).draw();
    });

    // ── Abrir modal para CRIAR ──────────────────────────────────────────────
    $('[data-bs-target="#modalCliente"]').on('click', function () {
        $('#modalClienteLabel').text('Novo Cliente');
        $('#clienteId').val('');
        $('#inputNome, #inputCPF, #inputTelefone, #inputEmail').val('');
    });


    // ── Abrir modal para EDITAR ─────────────────────────────────────────────
    $('#tabelaClientes').on('click', '.btn-editar', function () {
        const btn = $(this);
        $('#modalClienteLabel').text('Editar Cliente');
        $('#clienteId').val(btn.data('id'));
        $('#inputNome').val(btn.data('nome'));
        $('#inputCPF').val(btn.data('cpf'));
        $('#inputTelefone').val(btn.data('telefone'));
        $('#inputEmail').val(btn.data('email'));
        new bootstrap.Modal('#modalCliente').show();
    });


    // ── Salvar (criar ou editar) ────────────────────────────────────────────
    $('#btnSalvarCliente').on('click', function () {
        const id = $('#clienteId').val();
        const payload = {
            Nome:      $('#inputNome').val().trim(),
            CPF:       $('#inputCPF').val().trim(),
            Telefone:  $('#inputTelefone').val().trim(),
            Email:     $('#inputEmail').val().trim()
        };

        if (!payload.Nome || !payload.CPF) {
            alert('Nome e CPF são obrigatórios.');
            return;
        }

        const isEdicao = id !== '';
        $.ajax({
            url:         isEdicao ? `/cliente/${id}` : '/cliente/',
            type:        isEdicao ? 'PUT' : 'POST',
            contentType: 'application/json',
            data:        JSON.stringify(payload),
            success: function () {
                bootstrap.Modal.getInstance('#modalCliente').hide();
                tabela.ajax.reload();           // atualiza a tabela sem recarregar a página
            },
            error: function (xhr) {
                alert('Erro: ' + (xhr.responseJSON?.message ?? 'Tente novamente.'));
            }
        });
    });


    // ── Confirmar DELETE ────────────────────────────────────────────────────
    let idParaDeletar = null;

    $('#tabelaClientes').on('click', '.btn-deletar', function () {
        idParaDeletar = $(this).data('id');
        new bootstrap.Modal('#modalDelete').show();
    });

    $('#btnConfirmarDelete').on('click', function () {
        if (!idParaDeletar) return;

        $.ajax({
            url:  `/cliente/${idParaDeletar}`,
            type: 'DELETE',
            success: function () {
                bootstrap.Modal.getInstance('#modalDelete').hide();
                tabela.ajax.reload();
                idParaDeletar = null;
            },
            error: function (xhr) {
                alert('Erro ao deletar: ' + (xhr.responseJSON?.message ?? 'Tente novamente.'));
            }
        });
    });

});