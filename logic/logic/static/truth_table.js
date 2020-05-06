/**
 * truth_table.js
 * Andrew Ribeiro
 * May 5, 2020
**/

function addToFormula(elm){
    document.getElementById("formula").innerHTML += elm;
    makeTruthTable(document.getElementById("formula").innerHTML);
}

function deleteLast(){
    document.getElementById("formula").innerHTML = document.getElementById("formula").innerHTML .slice(0, -1);
    makeTruthTable(document.getElementById("formula").innerHTML);
}

function makeTruthTable(formula){
    $.ajax( {
        dataType: "json",
        url:"/test",
        data:{formula},
        success: function (data) {
            var container = document.getElementById("truthTable");

            if( data == null){
                container.innerHTML = "Invalid formula.";
                document.getElementById("formula").style.backgroundColor = "#fa8c8c";
            }else{
                container.innerHTML = "";
                var table = document.createElement("table")

                var row = document.createElement("tr");
                for(var i = 0; i < data.content.head.length; i++){
                    var cell = document.createElement("td");
                    cell.innerHTML = data.content.head[i];
                    row.appendChild(cell);
                }
                // Set formula style. -- sloppy
                row.lastChild.style.letterSpacing = "3px";
                table.appendChild(row);

                for(var i = 0; i < data.content.body.length; i++){
                    var row = document.createElement("tr");
                    for( var j = 0; j < data.content.body[i].length; j++){
                        var cell = document.createElement("td");
                        cell.innerHTML = data.content.body[i][j];
                        row.appendChild(cell);
                    }
                    table.appendChild(row);
                }

                container.appendChild(table);
                document.getElementById("formula").style.backgroundColor = "#a7fc8b";
            }
        }
     });
}