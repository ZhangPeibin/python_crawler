var fs = require("fs")


function saveHttpContent(file,data){
    fs.writeFile(file,data,{flag:'a'},function(err){
        if (err){
            return console.error(err)
        }

        console.log("数据写入成功")
    });
}

module.exports = {
  summary: 'a rule to hack response',
  *beforeSendResponse(requestDetail, responseDetail) {
    // 历史消息
    console.log(requestDetail.url)
    if (requestDetail.url.indexOf('https://mp.weixin.qq.com/mp/profile_ext') != -1) {
      const newResponse = responseDetail.response;
      var obj = JSON.stringify(requestDetail.requestData)
      saveHttpContent("1.txt",obj)
      return new Promise((resolve, reject) => {
        setTimeout(() => { // delay
          resolve({ response: newResponse });
        }, 5000);
      });
    }
  },
};