Date.prototype.Format = function(fmt)   {
    //author: meizz   
  var o = {
    "m+" : this.getMonth()+1,                 //月份   
    "d+" : this.getDate(),                    //日   
    "H+" : this.getHours(),                   //小时   
    "M+" : this.getMinutes(),                 //分   
    "S+" : this.getSeconds(),                 //秒   
    "q+" : Math.floor((this.getMonth()+3)/3), //季度   
    "s"  : this.getMilliseconds()             //毫秒   
  };    
  if(/(y+)/.test(fmt))   
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));   
  for(var k in o)   
    if(new RegExp("("+ k +")").test(fmt))   
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
  return fmt;   
} 
function millisecond_to_date(val, row){
    // 毫秒的时间戳转换为日期格式
    var date = new Date(parseInt(val));
    return date.Format('yyyy-m-d H:M:S');
}
function get_value_pair_from_formarray(form_array)
{
    // 获取form中对应的name:value对
    //form_array是一个数组  serializeArray 产生的 [Object, Object], 
    //返回一个JSON{'id':1, 'name':2 }
    var value_pair = {};
    for (index in form_array){
        value_pair[form_array[index].name] = form_array[index].value
    }
    return value_pair;
}



function  add_info_to_key(object){
    var new_data = JSON;
    for(k in object){
        new_data['info['+k+']']=object[k];
    }
    return new_data;
}


function  add_server_to_key(object){
    var new_data = JSON;
    for(k in object){
        new_data['info['+k+']']=object[k];
    }
    return new_data;
}
// 把Unicode编码转变为中文形式
// formatter:unicode_to_char
function unicode_to_char(value){
    x = value;

    var pattern = /\\u([\d\w]{4})/gi;
    x = x.replace(pattern, function (match, grp) { return String.fromCharCode(parseInt(grp, 16)); } );
    x = unescape(x);
     
    return x;
}
