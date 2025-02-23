import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

void main() {
  runApp(PokerApp());
}

class PokerApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Texas Hold\'em Poker',
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
  final _channel = WebSocketChannel.connect(Uri.parse('ws://localhost:8000/ws/Player_1'));
  String _gameMessage = "Waiting for players...";

  void _sendAction(String action, {int? amount}) {
    final data = {"player_id": "Player_1", "action": action, "amount": amount};
    _channel.sink.add(data.toString());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Poker Table')),
      body: Stack(
        children: [
          Positioned.fill(child: Image.asset("assets/poker_table.png", fit: BoxFit.cover)),
          Center(child: StreamBuilder(
            stream: _channel.stream,
            builder: (context, snapshot) {
              if (snapshot.hasData) _gameMessage = snapshot.data.toString();
              return Text(_gameMessage, style: TextStyle(fontSize: 20));
            },
          )),
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
