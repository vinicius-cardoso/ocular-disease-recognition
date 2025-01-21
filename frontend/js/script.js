let globalImage = null;

// document.addEventListener("DOMContentLoaded", function () {
//     const inputFile = document.getElementById("upload-img");
//     const processarBtn = document.getElementById("processar");
//     const carregaImg = document.getElementById("carrega-img");
//     const button = document.getElementById("processar");
//     const evolucaoImagem = document.getElementById("imagem");
//     const evolucaoResultado = document.getElementById("resultado");

//     processarBtn.addEventListener("click", function (event) {
//         event.preventDefault(); // Evita recarregar a página

//         if (inputFile.files.length > 0) {
//             button.classList.add("hidden");

//             carregaImg.innerHTML = `
//                 <div class="spinner-container">
//                     <div class="spinner"></div>
//                 </div>`;

//             // Simula o processamento por 3 segundos
//             setTimeout(() => {
//                 carregaImg.innerHTML = "<h2>Processamento concluído!</h2>";
//                 evolucaoImagem.classList.remove("active");
//                 evolucaoResultado.classList.add("active");
//             }, 10000);
//         } else {
//             alert("Por favor, selecione uma imagem antes de processar.");
//         }
//     });
// });

document.addEventListener("DOMContentLoaded", function () {
    const inputFile = document.getElementById("upload-img");
    const processarBtn = document.getElementById("processar");
    const carregaImg = document.getElementById("carrega-img");
    const button = document.getElementById("processar");
    const evolucaoImagem = document.getElementById("imagem");
    const evolucaoResultado = document.getElementById("resultado");

    processarBtn.addEventListener("click", function (event) {
        event.preventDefault();

        if (inputFile.files.length > 0) {
            button.classList.add("hidden");

            carregaImg.innerHTML = `
                <div class="spinner-container">
                <div class="spinner"></div>
                </div>
            `;

            const formData = new FormData();
            formData.append("image", inputFile.files[0]);

            fetch("/api/", {
                method: "POST",
                body: formData,
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(
                            `Erro na requisição: ${response.status}`
                        );
                    }
                    return response.json();
                })
                .then((data) => {
                    console.log("Resposta do servidor:", data);

                    // Simula o processamento após o envio
                    setTimeout(() => {
                        evolucaoImagem.classList.remove("active");
                        evolucaoResultado.classList.add("active");
                        carregaImg.classList.add("hidden");

                        const resultadoDoenca = document.createElement("div");
                        resultadoDoenca.classList.add("resultado-doenca");
                        resultadoDoenca.innerHTML = `
                            <p><strong>Resultado:</strong> ${data.label}</p>
                            <p><strong>Probabilidade:</strong> ${data.probability}%</p>
                            <img src="${globalImage}" alt="Imagem de Resultado"">
                        `;

                        main.appendChild(resultadoDoenca);
                    }, 1000);
                })
                .catch((error) => {
                    console.error("Erro na requisição:", error);
                    carregaImg.innerHTML =
                        "<h2>Erro ao processar a imagem. Tente novamente.</h2>";
                    button.classList.remove("hidden");
                });
        } else {
            alert("Por favor, selecione uma imagem antes de processar.");
        }
    });
});

// document.addEventListener("DOMContentLoaded", function () {
//     const inputFile = document.getElementById("upload-img");
//     const main = document.getElementById("main");
//     const processarBtn = document.getElementById("processar");
//     const carregaImg = document.getElementById("carrega-img");
//     const button = document.getElementById("processar");
//     const evolucaoImagem = document.getElementById("imagem");
//     const evolucaoResultado = document.getElementById("resultado");

//     processarBtn.addEventListener("click", function (event) {
//         event.preventDefault();

//         if (inputFile.files.length > 0) {
//             button.classList.add("hidden");

//             carregaImg.innerHTML = `
//                 <div class="spinner-container">
//                 <div class="spinner"></div>
//                 </div>
//             `;

//             // Simulação de resposta mockada
//             const mockResponse = new Promise((resolve) => {
//                 setTimeout(() => {
//                     resolve({
//                         probability: 95.32,
//                         label: "Retinopatia Diabética",
//                     });
//                 }, 2000); // Simula um tempo de resposta
//             });

//             mockResponse
//                 .then((data) => {
//                     console.log("Resposta mockada:", data);

//                     // Simula o processamento após o envio
//                     setTimeout(() => {
//                         evolucaoImagem.classList.remove("active");
//                         evolucaoResultado.classList.add("active");
//                         carregaImg.classList.add("hidden");

//                         const resultadoDoenca = document.createElement("div");
//                         resultadoDoenca.classList.add("resultado-doenca");
//                         resultadoDoenca.innerHTML = `
//                             <p><strong>Resultado:</strong> ${data.label}</p>
//                             <p><strong>Probabilidade:</strong> ${data.probability}%</p>
//                             <img src="${globalImage}" alt="Imagem de Resultado"">
//                         `;

//                         main.appendChild(resultadoDoenca);
//                     }, 1000);
//                 })
//                 .catch((error) => {
//                     console.error("Erro na requisição mockada:", error);
//                     carregaImg.innerHTML =
//                         "<h2>Erro ao processar a imagem. Tente novamente.</h2>";
//                     button.classList.remove("hidden");
//                 });
//         } else {
//             alert("Por favor, selecione uma imagem antes de processar.");
//         }
//     });
// });

document
    .getElementById("upload-img")
    .addEventListener("change", function (event) {
        const file = event.target.files[0];
        const preview = document.getElementById("preview-img");

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
                globalImage = e.target.result;
            };

            reader.readAsDataURL(file);
        }
    });
