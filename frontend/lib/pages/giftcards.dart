import 'dart:async';
import 'package:card_wallet/components/gift_card.dart';
import 'package:card_wallet/l10n/app_localizations.dart';
import 'package:flutter/material.dart';

class GiftCardListPage extends StatefulWidget {
  const GiftCardListPage({super.key});

  @override
  State<GiftCardListPage> createState() => _GiftCardListPageState();
}

class _GiftCardListPageState extends State<GiftCardListPage> {
  final List<GiftCardData> _giftcards = [];
  bool _isLoading = false;
  bool _hasMore = true;
  int _page = 0;
  final int _pageSize = 10;
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _fetchGiftCards();
    _scrollController.addListener(_scrollListener);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _fetchGiftCards({bool reset = false}) async {
    if (_isLoading) return;

    setState(() {
      _isLoading = true;
      if (reset) {
        _page = 0;
        _hasMore = true;
      }
    });

    // Mock network delay
    await Future.delayed(const Duration(seconds: 1));

    // Mock data generation
    final newItems = _hasMore
        ? List.generate(_pageSize, (i) {
            final id = _page * _pageSize + i;
            return GiftCardData(
              "Supplier $id",
              double.parse((10 + id).toString()),
              DateTime.now().add(Duration(days: id * 2)),
            );
          })
        : <GiftCardData>[];

    setState(() {
      if (reset) _giftcards.clear();
      _giftcards.addAll(newItems);
      _isLoading = false;
      _page++;
      if (newItems.length < _pageSize) _hasMore = false;
    });
  }

  void _scrollListener() {
    if (!_isLoading &&
        _hasMore &&
        _scrollController.position.pixels >=
            _scrollController.position.maxScrollExtent - 200) {
      _fetchGiftCards();
    }
  }

  Future<void> _onRefresh() async {
    await _fetchGiftCards(reset: true);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(AppLocalizations.of(context)!.giftCardPageTitle)),
      body: RefreshIndicator(
        onRefresh: _onRefresh,
        child: ListView.builder(
          controller: _scrollController,
          itemCount: _giftcards.length + 1,
          itemBuilder: (context, index) {
            if (index == _giftcards.length) {
              if (_isLoading) {
                return const Padding(
                  padding: EdgeInsets.all(16),
                  child: Center(child: CircularProgressIndicator()),
                );
              } else if (!_hasMore) {
                return Padding(
                  padding: EdgeInsets.all(16),
                  child: Center(
                    child: Text(
                      AppLocalizations.of(context)!.noMoreGiftCardText,
                      style: TextStyle(color: Colors.grey),
                    ),
                  ),
                );
              } else {
                return const SizedBox.shrink();
              }
            }

            final card = _giftcards[index];
            return GiftCardWidget(data: card);
          },
        ),
      ),
    );
  }
}
