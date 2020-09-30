import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:smartlock/main.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {

  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle.light.copyWith(statusBarColor: Colors.transparent));
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
              colors: [Colors.blue, Colors.teal],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter),
        ),
        child: _isLoading ? Center(child: CircularProgressIndicator()) : ListView(
          children: <Widget>[
            headerSection(),
            textSection(),
            buttonSection(),
            registerSection(),
          ],
        ),
      ),
    );
  }


  signIn(String email, pass) async {
    SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
    Map data = {
      'email': email,
      'password': pass
    };

    var jsonResponse = null;

    var response = await http.post("https://rmsf-smartlock.ew.r.appspot.com/toggle/Bruno/12345/12345", body: data);
    if(response.statusCode == 200) {
      jsonResponse = json.decode(response.body);
      print('aqua');
      print(response.body);

      if(jsonResponse != null) {
        setState(() {
          print('fixe');
          _isLoading = false;
        });
        print('saiu-> vai para outra pasta');
        sharedPreferences.setString("token", jsonResponse['token']);
        //Navigator.push(context, MaterialPageRoute(builder: (context) => SecondRoute()));
        //Navigator.pushNamed(context, ExtractArgumentsScreen.routeName, arguments: ScreenArguments('1', '2',) );
        Navigator.push(context, MaterialPageRoute(builder: (context) => SecondRoute()));
      }
    }
    else {
      setState(() {
        _isLoading = false;
      });
      print('fail');
      print(response.body);
    }
  }

  Container registerSection() {
    return Container(
      width: MediaQuery.of(context).size.width,
      height: 40.0,
      padding: EdgeInsets.symmetric(horizontal: 15.0),
      margin: EdgeInsets.only(top: 15.0),
      child: RaisedButton(
        elevation: 0.0,
        color: Colors.red,
        child: Text("Not registed? Register now!", style: TextStyle(color: Colors.white70)),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(5.0)),
        onPressed: () {

          Navigator.push(context, MaterialPageRoute(builder: (context) => Regist()));
        },

      ),
    );
  }

  Container buttonSection() {
    return Container(
      width: MediaQuery.of(context).size.width,
      height: 40.0,
      padding: EdgeInsets.symmetric(horizontal: 15.0),
      margin: EdgeInsets.only(top: 15.0),
      child: RaisedButton(
        onPressed: emailController.text == "" || passwordController.text == "" ? null : () {
          setState(() {
            _isLoading = true;
          });
          signIn(emailController.text, passwordController.text);
        },
        elevation: 0.0,
        color: Colors.purple,
        child: Text("Sign In", style: TextStyle(color: Colors.white70)),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(5.0)),
      ),
    );
  }

  final TextEditingController emailController = new TextEditingController();
  final TextEditingController passwordController = new TextEditingController();

  Container textSection() {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 15.0, vertical: 20.0),
      child: Column(
        children: <Widget>[
          TextFormField(
            controller: emailController,
            cursorColor: Colors.white,

            style: TextStyle(color: Colors.white70),
            decoration: InputDecoration(
              icon: Icon(Icons.email, color: Colors.white70),
              hintText: "Email",
              border: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white70)),
              hintStyle: TextStyle(color: Colors.white70),
            ),
          ),
          SizedBox(height: 30.0),
          TextFormField(
            controller: passwordController,
            cursorColor: Colors.white,
            obscureText: true,
            style: TextStyle(color: Colors.white70),
            decoration: InputDecoration(
              icon: Icon(Icons.lock, color: Colors.white70),
              hintText: "Password",
              border: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white70)),
              hintStyle: TextStyle(color: Colors.white70),
            ),
          ),
        ],
      ),
    );
  }

  Container headerSection() {
    return Container(
      margin: EdgeInsets.only(top: 50.0),
      padding: EdgeInsets.symmetric(horizontal: 20.0, vertical: 30.0),
      child: Text("Smartlock",
          style: TextStyle(
              color: Colors.white70,
              fontSize: 40.0,
              fontWeight: FontWeight.bold)),
    );
  }
}

class SecondRoute extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Controlo da porta"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            RaisedButton(
              child: Text("Abrir Porta"),
              onPressed: () {
                // vai para um sitio

              },
            ),
            RaisedButton(
              child: Text("Fechar Porta"),
              onPressed: () {
                //vai para outro sitio

              },
            ),
            RaisedButton(
              child: Text("Feed"),
              onPressed: () {
                //vai para outro sitio
                Navigator.push(context, MaterialPageRoute(builder: (context) => Notifica()));
              }
            ),
          ],
        )
      )
    );
  }
}


class Notifica extends StatelessWidget {
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle.light.copyWith(statusBarColor: Colors.transparent));
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
              colors: [Colors.blue, Colors.teal],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter),
        ),
        child: _isLoading ? Center(child: CircularProgressIndicator()) : ListView(
          children: <Widget>[
            headerSection_1(),
            notifica_get(),
          ],
        ),
      ),
    );
  }
}

Container notifica_get() {
  return Container(
      height: 40.0,
      padding: EdgeInsets.symmetric(horizontal: 15.0),
      margin: EdgeInsets.only(top: 15.0),
      child: RaisedButton(
        onPressed: () {
          busca_get();
        },
        elevation: 0.0,
        color: Colors.green,
        child: Text("Câmara"),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(5.0)),
      ),
  );
}

busca_get() async {
  var jsonResponse = null;

  print("estás aqui");

  final response = await http.get("https://rmsf-smartlock.ew.r.appspot.com/get/Bruno/12345/12345");

  if (response.statusCode == 200) {
    jsonResponse = json.decode(response.body);
    // If the server did return a 200 OK response,
    // then parse the JSON.
    print("temos get");
    print(response.body);
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load album');
  }
}



//other version
// A Widget that extracts the necessary arguments from the ModalRoute.
class ExtractArgumentsScreen extends StatelessWidget {

  static const routeName = '/extractArguments';

  @override
  Widget build(BuildContext context) {
    // Extract the arguments from the current ModalRoute settings and cast
    // them as ScreenArguments.
    final ScreenArguments args = ModalRoute.of(context).settings.arguments;

    return Scaffold(
      appBar: AppBar(
        title: Text(args.name),
      ),
      body: Center(
        child: Text(args.pass),
      ),
    );
  }
}

class ScreenArguments {
  final String name;
  final String pass;

  ScreenArguments(this.name, this.pass);
}

class Regist extends StatelessWidget {

  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle.light.copyWith(statusBarColor: Colors.transparent));
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
              colors: [Colors.blue, Colors.teal],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter),
        ),
        child: _isLoading ? Center(child: CircularProgressIndicator()) : ListView(
          children: <Widget>[
            headerSection_1(),
            textSection_1(),
            registerBottom(),
          ],
        ),
      ),
    );
  }
}


Container headerSection_1() {
  return Container(
    margin: EdgeInsets.only(top: 50.0),
    padding: EdgeInsets.symmetric(horizontal: 20.0, vertical: 30.0),
    child: Text("Smartlock",
        style: TextStyle(
            color: Colors.white70,
            fontSize: 40.0,
            fontWeight: FontWeight.bold)),
  );
}


final TextEditingController emailregister = new TextEditingController();
final TextEditingController passwordregister = new TextEditingController();
final TextEditingController idregister = new TextEditingController();

Container textSection_1() {
  return Container(
    padding: EdgeInsets.symmetric(horizontal: 15.0, vertical: 20.0),
    child: Column(
      children: <Widget>[
        TextFormField(
          controller: emailregister,
          cursorColor: Colors.white,
          style: TextStyle(color: Colors.white70),
          decoration: InputDecoration(
            icon: Icon(Icons.email, color: Colors.white70),
            hintText: "Email",
            border: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white70)),
            hintStyle: TextStyle(color: Colors.white70),
          ),
        ),
        SizedBox(height: 30.0),
        TextFormField(
          controller: passwordregister,
          cursorColor: Colors.white,
          obscureText: true,
          style: TextStyle(color: Colors.white70),
          decoration: InputDecoration(
            icon: Icon(Icons.lock, color: Colors.white70),
            hintText: "Password",
            border: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white70)),
            hintStyle: TextStyle(color: Colors.white70),
          ),
        ),
        TextFormField(
          controller: idregister,
          cursorColor: Colors.white,
          obscureText: true,
          style: TextStyle(color: Colors.white70),
          decoration: InputDecoration(
            icon: Icon(Icons.attachment, color: Colors.white70),
            hintText: "id",
            border: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white70)),
            hintStyle: TextStyle(color: Colors.white70),
          ),
        ),
      ],
    ),
  );
}

Container registerBottom() {
  return Container(
    height: 40.0,
    padding: EdgeInsets.symmetric(horizontal: 15.0),
    margin: EdgeInsets.only(top: 15.0),
    child: RaisedButton(
      onPressed: emailregister.text == "" || passwordregister.text == "" || idregister.text == "" ? null : () {
        registIn(emailregister.text, passwordregister.text, idregister.text);
      },
      elevation: 0.0,
      color: Colors.purple,
      child: Text("Regist", style: TextStyle(color: Colors.white70)),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(5.0)),
    ),
  );
}

registIn(String email, pass, id) async {
  SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
  Map data = {
    'email': email,
    'password': pass,
    'id' : id
  };
  var jsonResponse = null;

  var path = "https://rmsf-smartlock.ew.r.appspot.com/register/"+ email + "/" + pass + "/" + id;

  print(path);

  var response = await http.post(path, body: data);
  if(response.statusCode == 200) {
    jsonResponse = json.decode(response.body);
    print('aqua');
    print(response.body);

    if(jsonResponse != null) {
      /*setState(() {
        print('fixe');
        _isLoading = false;
      });*/
      print('saiu-> vai para outra pasta');
      sharedPreferences.setString("token", jsonResponse['token']);
      //Navigator.push(context, MaterialPageRoute(builder: (context) => SecondRoute()));
      //Navigator.pushNamed(context, ExtractArgumentsScreen.routeName, arguments: ScreenArguments('1', '2',) );
      // Navigator.push(context, MaterialPageRoute(builder: (context) => SecondRoute()));
    }
  }
  else {
    /*setState(() {
      _isLoading = false;
    });*/
    print('fail');
    print(response.body);
  }
}