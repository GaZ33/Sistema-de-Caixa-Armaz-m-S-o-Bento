// Funções para realizar operações CRUD na página de Gestão de Produtos

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("product-modal");
    const addButton = document.getElementById("add-product-button");
    const closeButton = document.querySelector(".close-button");
    const deleteButton = document.getElementById("delete-product-button");

    // Inicializa DataTables
    const productTable = $("#product-table").DataTable();

    addButton.addEventListener("click", () => {
        abrirModal("Adicionar Produto");
    });

    closeButton.addEventListener("click", fecharModal);

    deleteButton.addEventListener("click", () => {
        const id = document.getElementById("product-id").value;
        deletarProduto(id);
    });

    carregarProdutos();

    const form = document.getElementById("form-product");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        const id = document.getElementById("product-id").value;
        if (id) {
            atualizarProduto(id);
        } else {
            criarProduto();
        }
    });
});

// Função para buscar produtos
function buscarProdutos() {
    const query = document.getElementById("search-query").value;
    fetch(`/api/produtos/buscar?query=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            listarProdutos(data);
        })
        .catch(error => console.error("Erro ao buscar produtos:", error));
}

// Função para listar produtos na tabela
function listarProdutos(produtos) {
    const tbody = document.querySelector("#product-list tbody");
    tbody.innerHTML = "";
    produtos.forEach(produto => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${produto.id}</td>
            <td>${produto.nome}</td>
            <td>${produto.preco_unidade}</td>
            <td>${produto.unidade}</td>
            <td>${produto.codigo}</td>
            <td>${produto.marca}</td>
            <td>
                <button onclick="editarProduto(${produto.id})">Editar</button>
                <button onclick="deletarProduto(${produto.id})">Deletar</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Função para carregar produtos na tabela
function carregarProdutos() {
    fetch("/api/produtos")
        .then(response => response.json())
        .then(data => {
            const productTable = $("#product-table").DataTable();
            productTable.clear();
            data.forEach(produto => {
                productTable.row.add([
                    produto.id,
                    produto.nome,
                    produto.preco_unidade,
                    produto.unidade,
                    produto.codigo,
                    produto.marca,
                    `<button onclick="editarProduto(${produto.id})">Editar</button>`
                ]).draw();
            });
        })
        .catch(error => console.error("Erro ao carregar produtos:", error));
}

// Função para criar um novo produto
function criarProduto() {
    const produto = obterDadosFormulario();

    fetch("/api/produtos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(produto)
    })
        .then(response => {
            if (response.ok) {
                carregarProdutos();
                limparFormulario();
            } else {
                console.error("Erro ao criar produto");
            }
        })
        .catch(error => console.error("Erro ao criar produto:", error));
}

// Função para editar um produto
function editarProduto(id) {
    fetch(`/api/produtos/${id}`)
        .then(response => response.json())
        .then(produto => {
            document.getElementById("product-id").value = produto.id;
            document.getElementById("product-name").value = produto.nome;
            document.getElementById("product-price").value = produto.preco_unidade;
            document.getElementById("product-quantity").value = produto.quantidade;
            document.getElementById("product-unit").value = produto.unidade;
            document.getElementById("product-code").value = produto.codigo;
            document.getElementById("product-brand").value = produto.marca;
            abrirModal("Editar Produto");
            document.getElementById("delete-product-button").style.display = "block";
        })
        .catch(error => console.error("Erro ao carregar produto:", error));
}

// Função para atualizar um produto
function atualizarProduto(id) {
    const produto = obterDadosFormulario();

    fetch(`/api/produtos/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(produto)
    })
        .then(response => {
            if (response.ok) {
                carregarProdutos();
                limparFormulario();
            } else {
                console.error("Erro ao atualizar produto");
            }
        })
        .catch(error => console.error("Erro ao atualizar produto:", error));
}

// Função para deletar um produto
function deletarProduto(id) {
    fetch(`/api/produtos/${id}`, {
        method: "DELETE"
    })
        .then(response => {
            if (response.ok) {
                carregarProdutos();
            } else {
                console.error("Erro ao deletar produto");
            }
        })
        .catch(error => console.error("Erro ao deletar produto:", error));
}

// Função para obter os dados do formulário
function obterDadosFormulario() {
    return {
        nome: document.getElementById("product-name").value,
        preco: parseFloat(document.getElementById("product-price").value),
        quantidade: parseInt(document.getElementById("product-quantity").value, 10),
        unidade: document.getElementById("product-unit").value,
        marca: document.getElementById("product-brand").value
    };
}

// Função para limpar o formulário
function limparFormulario() {
    document.getElementById("product-id").value = "";
    document.getElementById("product-name").value = "";
    document.getElementById("product-price").value = "";
    document.getElementById("product-quantity").value = "";
    document.getElementById("product-unit").value = "";
    document.getElementById("product-brand").value = "";
}

// Modal
function abrirModal(id) {
    document.getElementById(id).classList.add('aberto');
}

function fecharModal(id) {
    document.getElementById(id).classList.remove('aberto');
}

function cadastrarProduto() {
    const dados = {
        nome: document.getElementById('cad-prod-nome').value,
        marca: document.getElementById('cad-prod-marca').value,
        quantidade: document.getElementById('cad-prod-quantidade').value,
        quantidade_min: document.getElementById('cad-prod-quantidade-min').value,
        preco: document.getElementById('cad-prod-preco').value,
    };

    console.log("Cadastrar produto:", dados);
    // quando ligar ao backend: fetch('/api/produtos', { method: 'POST', body: JSON.stringify(dados) })

    fecharModal('modal-cadastrar-produto');
}