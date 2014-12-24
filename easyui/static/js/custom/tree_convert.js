// generate tree menu
function tree_convert(rows){
    var nodes = [];

    // get the top level nodes
    // if is_root is true , it's top level node.
    // for(var i=0; i<rows.length; i++){
    //     var row = rows[i];
    //     if (row.is_root ==  true){
    //         nodes.push(row);
    //     }
    // }
    for(var i=rows.length-1; i>=0; i--){
        var row = rows[i];
        if (row.is_root ==  true){
            nodes.unshift(row);
            rows.splice(i,1)
        }

    }
    
    var toDo = [];
    for(var i=0; i<nodes.length; i++){
        toDo.push(nodes[i]);
    }
    while(toDo.length){
        var node = toDo.shift();    // the parent node
        // get the children nodes
        for(var i=0; i<rows.length; i++){
            var row = rows[i];
            if (row.parent_id == node.id ){
                
                //var child = {id:row.id,text:row.name};
                var child = row;
                if (node.children){
                    node.children.push(child);
                } else {
                    node.children = [child];
                }
                toDo.push(child);
            }
        }
    }
    return nodes;
}
