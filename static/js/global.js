document.addEventListener("DOMContentLoaded", function() {

    const choiceModal = document.getElementById("choiceModal");
    const masukModal = document.getElementById("masukModal");
    const keluarModal = document.getElementById("keluarModal");
    const openChoiceBtn = document.getElementById("openChoice");

    if (openChoiceBtn) {
        openChoiceBtn.addEventListener("click", function() {
            choiceModal.classList.add("active");
        });
    }

    document.querySelectorAll(".open-masuk").forEach(btn => {
        btn.addEventListener("click", function() {
            choiceModal.classList.remove("active");
            masukModal.classList.add("active");
        });
    });

    document.querySelectorAll(".open-keluar").forEach(btn => {
        btn.addEventListener("click", function() {
            choiceModal.classList.remove("active");
            keluarModal.classList.add("active");
        });
    });

    document.querySelectorAll(".close-modal").forEach(btn => {
        btn.addEventListener("click", function() {
            choiceModal.classList.remove("active");
            masukModal.classList.remove("active");
            keluarModal.classList.remove("active");
        });
    });

});