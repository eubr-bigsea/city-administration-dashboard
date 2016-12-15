function RestClient() {
    this.getRestURL = function () {
        var REST_URL = location.protocol;
        REST_URL += "//";
        REST_URL += location.host;

        return REST_URL;
    };

    this.login = function (matricula, senha, callback) {
        var data = {};
        data['matricula'] = matricula;
        data['senha'] = senha;

        $.ajax({
            url: this.getRestURL() + "/login",
            method: "POST",
            contentType: 'application/json; charset=UTF-8',
            data: JSON.stringify(data)
        }).done(function (data) {
            if (data == 'true') {
                callback(true);
            }

            if (data == 'false') {
                callback(false);
            }
        }).fail(function () {
            // TODO: tratar isso aqui
            alert("Ocorreu um erro!");
        });
    };

    this.getListaDeEscalas = function (callback) {
        $.ajax({
            url: this.getRestURL() + "/api/v1/escalas/",
            method: "GET",
            dataType: "json"
        }).done(function (data) {
            callback(data);
        }).fail(function () {
            // TODO: tratar isso aqui
            alert("Ocorreu um erro!");
        });
    };

    this.getLocaisDeFiscalizacoes = function (callback){
        $.ajax({
            url: this.getRestURL() + "/api/v1/pontos_de_fiscalizacao/",
            method: "GET",
            dataType: "json"
        }).done(function (data) {
            callback(data);
        }).fail(function () {
            // TODO: tratar isso aqui
            alert("Ocorreu um erro!");
        });
    };

    this.getTodosFiscais = function (callback){
        $.ajax({
            url: this.getRestURL() + "/api/v1/usuarios/",
            method: "GET",
            dataType: "json"
        }).done(function (data) {
            callback(data);

        }).fail(function () {
            // TODO: tratar isso aqui
            alert("Ocorreu um erro!");
        });
    };


}
