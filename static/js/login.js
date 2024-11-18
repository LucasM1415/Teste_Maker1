document.querySelector("#loginForm").addEventListener("submit", async (e) => {
    e.preventDefault(); // Impede o envio padrão do formulário
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Convertendo FormData para um objeto JSON
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(form.action, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",  // Envia os dados como JSON
            },
            body: JSON.stringify(data),  // Converte os dados para JSON
        });
    
        const result = await response.json();
        const messageElement = document.getElementById("message");

        if (response.ok) {
            // Exibe a mensagem de sucesso
            messageElement.textContent = result.message;
            messageElement.style.color = "green";

            // Redireciona para o dashboard após login bem-sucedido
            if (result.message.includes("Admin")) {
                window.location.href = "/admin_dashboard"; // Caminho da rota do dashboard do admin
            } else {
                window.location.href = "/dashboard"; // Caminho da rota do dashboard do usuário
            }
        } else {
            // Exibe o erro, se houver
            messageElement.textContent = result.error || "Erro ao fazer login.";
            messageElement.style.color = "red";
        }
    } catch (error) {
        console.error("Erro ao enviar formulário:", error);

        // Mensagem genérica para erros no envio
        const messageElement = document.getElementById("message");
        messageElement.textContent = "Erro inesperado. Tente novamente.";
        messageElement.style.color = "red";
    }
});
