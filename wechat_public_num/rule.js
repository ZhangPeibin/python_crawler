var fs = require("fs")
var exec = require("child_process").exec;
var url = require("url")

function execPythonToDealHtml(file,offset){
    var python_name = "html_process.py"
    exec('python'+' '+python_name + ' '+file+' '+offset,function(err,stdout,stderr){
    if(err)
        {
            console.log('stderr',err);
        }

    if(stdout)
        {
            console.log('stdout',stdout);
        }
    });
}

function saveHttpContent(file,data,offset){
    var f = "tmp/"+file
    fs.writeFile(f,data,{flag:'w'},function(err){
        if (err){
            return console.error(err)
        }
        console.log("数据写入成功")
        console.log("开始解析公众号数据")
        execPythonToDealHtml(f,offset)
    });
}

var home = "https://mp.weixin.qq.com/mp/profile_ext?action=home"
var getmsg = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg"

module.exports = {
  summary: 'a rule to hack response',
  *beforeSendResponse(requestDetail, responseDetail) {
    // 历史消息
    if (requestDetail.url.indexOf(home) != -1 ||
        requestDetail.url.indexOf(getmsg) != -1) {

        offset = 0
        if (requestDetail.url.indexOf(home) != -1){
            offset = 0
        }else if(requestDetail.url.indexOf(getmsg) != -1){
            var path = url.parse(requestDetail.url,true).query
            offset = path.offset
        }
        const newResponse = responseDetail.response;
        var obj = JSON.stringify(newResponse)
        saveHttpContent(offset+".html",responseDetail.response.body,offset)
        return new Promise((resolve, reject) => {
            setTimeout(() => { // delay
            resolve({ response: newResponse });
            }, 5000);
        });
    }
  },
};