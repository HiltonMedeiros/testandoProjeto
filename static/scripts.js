document.addEventListener("DOMContentLoaded", function () {
    let pessoaSelect = document.getElementById("pessoa_id");
    let tipoSelect = document.getElementById("tipo");

    function atualizarOpcoesTipo() {
        let pessoaSelecionada = pessoaSelect.options[pessoaSelect.selectedIndex];
        let idade = parseInt(pessoaSelecionada.getAttribute("data-idade"));

        // LIMPA SELECT
        tipoSelect.innerHTML = "";

        if (idade < 18) {
            //MENOR DE IDADE = DESPESA
            let option = document.createElement("option");
            option.value = "despesa";
            option.textContent = "Despesa";
            tipoSelect.appendChild(option);
        } else {
            // MAIOR DE IDADE = RECEITA E DESPESA
            ["receita", "despesa"].forEach(tipo => {
                let option = document.createElement("option");
                option.value = tipo;
                option.textContent = tipo.charAt(0).toUpperCase() + tipo.slice(1);
                tipoSelect.appendChild(option);
            });
        }
    }
    atualizarOpcoesTipo();

    // ATUALIZA OPÇÕES SEMPRE QUE MUDAR O SELECT
    pessoaSelect.addEventListener("change", atualizarOpcoesTipo);
});
