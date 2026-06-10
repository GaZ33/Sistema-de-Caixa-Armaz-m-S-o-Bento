import os, re

files = [
    'app/app/templates/produto/index.html',
    'app/app/templates/Ponto_de_venda/index.html',
    'app/app/templates/home/index.html',
    'app/app/templates/contas_cliente/index.html',
    'app/app/templates/clientes/index.html'
]

insert_block = '''
    <div class="nav-group">
        <a href="/vendas/index.html" class="topbar-btn">
            <img src="/static/icones/Sim.png" alt="Vendas">
            VENDAS
        </a>
    </div>'''

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    target1 = '''<div class="nav-group">
        <a href="/ponto-de-venda/index.html" class="topbar-btn">
            <img src="/static/icones/Sim.png" alt="PDV">
            PDV
        </a>
    </div>'''
    
    target2 = '''<div class="nav-group">
        <a href="/ponto-de-venda/index.html" class="topbar-btn active">
            <img src="/static/icones/Sim.png" alt="PDV">
            PDV
        </a>
    </div>'''
    
    if target1 in content:
        content = content.replace(target1, target1 + insert_block)
        print('Patched', f)
    elif target2 in content:
        content = content.replace(target2, target2 + insert_block)
        print('Patched', f)
    else:
        pattern = re.compile(r'(<div class="nav-group">\s*<a href="/ponto-de-venda/index\.html" class="topbar-btn(?: active)?">\s*<img src="/static/icones/Sim\.png" alt="PDV">\s*PDV\s*</a>\s*</div>)')
        if pattern.search(content):
            content = pattern.sub(r'\1' + insert_block, content)
            print('Patched with Regex', f)
        else:
            print('Could not find PDV block in', f)
            
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
