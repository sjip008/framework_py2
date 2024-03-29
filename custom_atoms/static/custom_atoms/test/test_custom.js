(function(){
    $.atoms.self_server_get_dfusage = [
        {
            tag_code: "self_server_ip",
            type: "input",
            attrs: {
                name: "主机IP",
                hookable: true,
                default: '10.0.1.192',
                validation: [
                    {
                        type: "required"
                    }
                ]
            },
        },
        {
            tag_code: "self_server_system",
            type: "input",
            attrs: {
                name: "主机系统",
                default: "linux centos",
                hookable: true,
                validation: [
                    {
                        type: "required"
                    }
                ]
            }
        },
        {
            tag_code: "self_server_disk",
            type: "input",
            attrs: {
                name: "主机磁盘",
                hookable: true,
                default: '/',
                validation: [
                    {
                        type: "required"
                    }
                ]
            },
        },
    ]
})();