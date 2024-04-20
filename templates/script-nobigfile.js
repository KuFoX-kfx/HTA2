const uploadField = document.getElementById("banner");
uploadField.onchange = function() {
    if(this.files[0].size > 2097152) {
       alert("Файл очень большой!");
    }
};