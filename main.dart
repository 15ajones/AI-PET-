import 'dart:convert';

import 'package:english_words/english_words.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;

void sendDataToRaspberryPi(Map<String, dynamic> requestData) async {
  var url = 'http://172.20.10.13:5000/data'; //'http://localhost:5000/data';
  print(requestData);
  //var response = await http.post(Uri.parse(url), body: {'data': data});
  print("CHECK");
  var response = await http.post(
    Uri.parse(url),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode(requestData),
  );
  print("hi");
  if (response.statusCode == 200) {
    // Data successfully sent to the Raspberry Pi
    print("success");
  } else {
    // Error occurred during data transmission
    print("error sending data");
  }
}
// Uncomment lines 3 and 6 to view the visual layout at runtime.
// import 'package:flutter/rendering.dart' show debugPaintSizeEnabled;

void main() {
  // debugPaintSizeEnabled = true;
  runApp(const MyCustomForm());
}

/*class MyCustomForm extends StatefulWidget {
  const MyCustomForm({super.key});

  @override
  MyCustomFormState createState() {
    return MyCustomFormState();
  }
}*/

class MyCustomForm extends StatefulWidget {
  const MyCustomForm({Key? key}) : super(key: key);

  @override
  MyCustomFormState createState() {
    return MyCustomFormState();
  }
}

bool validateEmail(String email) {
  // Regular expression pattern for email validation
  final RegExp emailRegex = RegExp(
      r'^[\w-]+(\.[\w-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$');

  return emailRegex.hasMatch(email);
}

//String selectedOption;
// Define a corresponding State class.
// This class holds data related to the form.
final _formKey = GlobalKey<FormState>();

final nameController = TextEditingController();
final emailController = TextEditingController();
final contactController = TextEditingController();
final locationController = TextEditingController();
final animalController = TextEditingController();
final spUsernameController = TextEditingController();
final spPasswordController = TextEditingController();
String animalOption = "cat`";

class MyCustomFormState extends State<MyCustomForm> {
  @override
  Widget build(BuildContext context) {
    String selectedOption =
        "Cat"; // Build a Form widget using the _formKey created above.
    List<String> options = ['cat', 'dog'];

    Widget nameSection = Container(
      padding: const EdgeInsets.all(8),
      child: Row(
        // children: [
        // Expanded(
        /*1*/
        // child: Column(
        // crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          /*2*/
          //children: [
          Text('Name:'),
          SizedBox(
              width:
                  10), // Add some spacing between the text and the TextFormField
          Expanded(
            child: TextFormField(
              // Add your TextFormField properties here
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                //hintText: 'Enter your name',
              ),
              controller: nameController,
              // The validator receives the text that the user has entered.
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
          ),
        ],
      ),
    );

    Color color = Theme.of(context).primaryColor;
    bool validateEmail(String email) {
      // Regular expression pattern for email validation
      final RegExp emailRegex = RegExp(
          r'^[\w-]+(\.[\w-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$');

      return emailRegex.hasMatch(email);
    }

    Widget emailSection = Container(
      padding: const EdgeInsets.all(8),
      child: Row(
        // children: [
        // Expanded(
        /*1*/
        // child: Column(
        // crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          /*2*/
          //children: [
          Text('Gmail:'),
          SizedBox(
              width:
                  10), // Add some spacing between the text and the TextFormField
          Expanded(
            child: TextFormField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                // hintText: 'Enter your gmail address',
              ),
              controller: emailController,
              // The validator receives the text that the user has entered.
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                if (!validateEmail(value)) {
                  return 'Invalid email address';
                }
                return null;
              },
            ),
          ),
        ],
      ),
    );

    Widget spotifyUsername = Container(
      padding: const EdgeInsets.all(8),
      child: Row(
        // children: [
        // Expanded(
        /*1*/
        // child: Column(
        // crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          /*2*/
          //children: [
          Text('Spotify Username:'),
          SizedBox(
              width:
                  10), // Add some spacing between the text and the TextFormField
          Expanded(
            child: TextFormField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                // hintText: 'Enter your gmail address',
              ),
              controller: spUsernameController,
              // The validator receives the text that the user has entered.
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
          ),
        ],
      ),
    );

    Widget spotifyPassword = Container(
      padding: const EdgeInsets.all(8),
      child: Row(
        // children: [
        // Expanded(
        /*1*/
        // child: Column(
        // crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          /*2*/
          //children: [
          Text('Spotify Password:'),
          SizedBox(
              width:
                  10), // Add some spacing between the text and the TextFormField
          Expanded(
            child: TextFormField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                // hintText: 'Enter your gmail address',
              ),
              controller: spPasswordController,
              // The validator receives the text that the user has entered.
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
          ),
        ],
      ),
    );

    Widget contactSection = Container(
      padding: const EdgeInsets.all(8),
      child: Row(
        // children: [
        // Expanded(
        /*1*/
        // child: Column(
        // crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          /*2*/
          //children: [
          Text('Emergency Contact Number:'),
          SizedBox(
              width:
                  10), // Add some spacing between the text and the TextFormField
          Expanded(
            child: TextFormField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.blue),
                ),
                // hintText: 'Enter your emergency contact number',
              ),
              controller: contactController,
              // The validator receives the text that the user has entered.
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
          ),
        ],
      ),
    );
    Widget animalpref = Container(
      padding: const EdgeInsets.all(8),
      child: Row(
        // children: [
        // Expanded(
        /*1*/
        // child: Column(
        // crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          /*2*/
          //children: [
          Text('Animal Preference'),
          SizedBox(
              width:
                  10), // Add some spacing between the text and the TextFormField
          Expanded(
              child: DropdownButtonFormField<String>(
            value: selectedOption,
            onChanged: (String? newValue) {
              setState(() {
                selectedOption = newValue!;
              });
            },
            items: options.map((String value) {
              return DropdownMenuItem<String>(
                value: value,
                child: Text(value),
              );
            }).toList(),
            /*decoration: InputDecoration(
              labelText: 'AI PET animal preference',
            ),*/
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Please select an option';
              }
              return null;
            },
            onSaved: (value) {
              // Handle the selected option
              selectedOption = value!;
            },
          ))
        ],
      ),
    );
    Widget submitButton = Padding(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: ElevatedButton(
        onPressed: () {
          // Validate returns true if the form is valid, or false otherwise.
          if (_formKey.currentState!.validate()) {
            _formKey.currentState!.save();

            Map<String, dynamic> requestData = {
              'name': nameController.text,
              'email': emailController.text,
              'contact': contactController.text,
              'location': locationController.text,
              'spotify username': spUsernameController.text,
              'spotify password': spPasswordController.text,
              'animal': selectedOption,
            };

            sendDataToRaspberryPi(requestData);
          }
        },
        child: const Text('Submit'),
      ),
    );

    Widget locationSection = Container(
      padding: const EdgeInsets.all(8),
      child: Row(
        // children: [
        // Expanded(
        /*1*/
        // child: Column(
        // crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          /*2*/
          //children: [
          Text('City:'),
          SizedBox(
              width:
                  10), // Add some spacing between the text and the TextFormField
          Expanded(
            child: TextFormField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                //hintText: 'Enter your location',
              ),
              controller: locationController,
              // The validator receives the text that the user has entered.
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter some text';
                }
                return null;
              },
            ),
          ),
        ],
      ),
    );

    return Form(
      key: _formKey,
      child: MaterialApp(
        title: 'AI PET NoVa',
        home: Scaffold(
          appBar: AppBar(
            title: const Text('AI PET NoVa'),
          ),
          body: ListView(
            padding: EdgeInsets.symmetric(vertical: 2),
            children: [
              Image.asset(
                'assets/images/image no bg.png',
                width: 300,
                height: 160,
                // fit: BoxFit.cover,
              ),
              SizedBox(height: 2),
              nameSection,
              SizedBox(height: 2),
              emailSection,
              SizedBox(height: 2),
              contactSection,
              SizedBox(height: 2),
              locationSection,
              SizedBox(height: 2),
              spotifyUsername,
              SizedBox(height: 2),
              spotifyPassword,
              SizedBox(height: 2),
              animalpref,
              SizedBox(height: 2),
              submitButton,
            ],
          ),
        ),
      ),
    );
  }
}
