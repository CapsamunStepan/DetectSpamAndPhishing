document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        closeModal();
    }, 8000); // Закрытие через 3 секунды
});

function closeModal() {
    let modal = document.getElementById("modal");
    modal.style.opacity = "0";
    setTimeout(() => {
        modal.style.display = "none";
    }, 500); // Плавное исчезновение
}
