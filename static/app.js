


window.onload = function(){
    const qvars = document.getElementById("qvars");
    qvars.innerHTML = "a b c";

    const formulaInput = document.getElementById("formula");

    var updateVars = function(){
        var chars = formulaInput.value.split("");
        chars = chars.filter(char => /[a-z]/.test(char));
        chars = [... new Set(chars)];
        qvars.innerHTML = chars.join(" ");
    };

    updateVars();

    formulaInput.addEventListener("keyup", function(){
        updateVars();
       
    });
}