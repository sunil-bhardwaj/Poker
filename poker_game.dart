import 'package:flutter/material.dart';
import 'package:flutter_web_socket/flutter_web_socket.dart';

void main() {
  runApp(PokerApp());
}

class PokerApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Poker Game',
      theme: ThemeData.dark(),
      home: PokerTableScreen(),
    );
  }
}

class PokerTableScreen extends StatefulWidget {
  @override
  _PokerTableScreenState createState() => _PokerTableScreenState();
}

class _PokerTableScreenState extends State<PokerTableScreen> {
  late WebSocket _socket;
  String _gameMessage = "Waiting for players...";

  @override
  void initState() {
    super.initState();
    _connectWebSocket();
  }

  void _connectWebSocket() {
    _socket = WebSocket('ws://localhost:8765');
    _socket.onMessage((message) {
      setState(() {
        _gameMessage = message;
      });
    });
  }

  void _sendAction(String action, {int? amount}) {
    Map<String, dynamic> data = {
      "player_id": "Player_1",
      "action": action,
      "amount": amount
    };
    _socket.send(data.toString());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Texas Hold\'em Poker')),
      body: Stack(
        children: [
          Positioned.fill(child: Image.asset("assets/poker_table_3d.png", fit: BoxFit.cover)),
          Center(child: Text(_gameMessage, style: TextStyle(fontSize: 20))),
          Align(
            alignment: Alignment.bottomCenter,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(onPressed: () => _sendAction("fold"), child: Text("Fold")),
                ElevatedButton(onPressed: () => _sendAction("check"), child: Text("Check")),
                ElevatedButton(onPressed: () => _sendAction("bet", amount: 50), child: Text("Bet 50")),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
