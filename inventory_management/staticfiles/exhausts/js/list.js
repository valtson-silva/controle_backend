const select = document.getElementById("option-list")

function createOptions(list) {
    for (let i = 0; i < list.length; i++) {
        const option = document.createElement("option")
        option.textContent = list[i]
        select.append(option)
    }
}

async function OptionsModels() {
    const response = await fetch("http://127.0.0.1:8000/modelo_de_carro/")
    list = await response.then((res) => res.json())
    createOptions(list)
}