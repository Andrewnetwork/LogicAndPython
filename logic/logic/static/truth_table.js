  function addToFormula(elm){
    document.getElementById("formula").innerHTML += elm;
    makeTruthTable(document.getElementById("formula").innerHTML);
  }
  function deleteLast(){
    document.getElementById("formula").innerHTML = document.getElementById("formula").innerHTML .slice(0, -1);
  }
  function makeTruthTable(formula){
    var jqxhr = $.ajax( {
        dataType: "json",
        url:"/test",
        data:{formula},
        success: function (data) {
            var container = document.getElementById("truthTable");
            container.innerHTML = "";
            var table = document.createElement("table")

            var row = document.createElement("tr");
            for(var i = 0; i < data.content.head.length; i++){
                var cell = document.createElement("td");
                cell.innerHTML = data.content.head[i];
                row.appendChild(cell);
            }
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
        }
     });
  }