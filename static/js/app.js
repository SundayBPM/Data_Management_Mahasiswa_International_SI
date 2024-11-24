document.addEventListener("DOMContentLoaded", function() {
    const role = document.getElementById('role').value; // Ambil role dari elemen hidden
    const readonlyInputs = document.querySelectorAll('#status, #intake_year, #intake, #from, #until');

    if (role === 'dosen') {
        // Jika role adalah 'dosen', hilangkan atribut readonly
        readonlyInputs.forEach(function(input) {
            input.removeAttribute('readonly');
        });
    } else if (role === 'mahasiswa') {
        // Jika bukan 'dosen', buat semua input read-only
        readonlyInputs.forEach(function(input) {
            input.setAttribute('readonly', true);
        });
    }
});



