import 'package:card_wallet/l10n/app_localizations.dart';
import 'package:flutter/material.dart';
import 'dart:async';

class UploadPage extends StatefulWidget {
  const UploadPage({super.key});

  @override
  State<UploadPage> createState() => _UploadPageState();
}

class _UploadPageState extends State<UploadPage> {
  final _formKey = GlobalKey<FormState>();
  bool _uploading = false;
  String? _selectedFileName;

  // Form fields
  final _supplierController = TextEditingController();
  final _amountController = TextEditingController();
  DateTime? _expirationDate;

  Future<void> _mockPickFile() async {
    // Simulate file selection
    await Future.delayed(const Duration(milliseconds: 500));
    setState(() {
      _selectedFileName = "giftcard_example.pdf";
    });
  }

  Future<void> _mockUpload() async {
    if (!_formKey.currentState!.validate() || _selectedFileName == null) return;

    setState(() => _uploading = true);

    // Simulate upload delay
    await Future.delayed(const Duration(seconds: 2));

    setState(() => _uploading = false);

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(AppLocalizations.of(context)!.giftCardUploadSuccessText)),
      );
    }
  }

  Future<void> _pickDate() async {
    final now = DateTime.now();
    final picked = await showDatePicker(
      context: context,
      initialDate: now,
      firstDate: now.subtract(const Duration(days: 365)),
      lastDate: now.add(const Duration(days: 365 * 5)),
    );

    if (picked != null) {
      setState(() {
        _expirationDate = picked;
      });
    }
  }

  @override
  void dispose() {
    _supplierController.dispose();
    _amountController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(AppLocalizations.of(context)!.giftCardUploadText)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                controller: _supplierController,
                decoration: InputDecoration(
                  labelText: AppLocalizations.of(context)!.supplierText,
                  border: OutlineInputBorder(),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? AppLocalizations.of(context)!.supplierValidationText : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _amountController,
                decoration: InputDecoration(
                  labelText: AppLocalizations.of(context)!.amountFormText,
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) return AppLocalizations.of(context)!.amountValidationText;
                  final n = num.tryParse(value);
                  if (n == null || n <= 0) return AppLocalizations.of(context)!.amountWrongText;
                  return null;
                },
              ),
              const SizedBox(height: 16),
              InkWell(
                onTap: _pickDate,
                child: InputDecorator(
                  decoration: InputDecoration(
                    labelText: AppLocalizations.of(context)!.expirationDateFormText,
                    border: OutlineInputBorder(),
                  ),
                  child: Text(
                    _expirationDate == null
                        ? AppLocalizations.of(context)!.expirationDateFormTooltip
                        : "${_expirationDate!.day}/${_expirationDate!.month}/${_expirationDate!.year}",
                  ),
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                icon: const Icon(Icons.attach_file),
                label: Text(AppLocalizations.of(context)!.fileFormText),
                onPressed: _uploading ? null : _mockPickFile,
              ),
              const SizedBox(height: 10),
              if (_selectedFileName != null)
                Text(
                  "Selected: $_selectedFileName",
                  textAlign: TextAlign.center,
                  style: theme.textTheme.bodyLarge,
                ),
              const SizedBox(height: 40),
              FilledButton.icon(
                icon: _uploading
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.cloud_upload),
                label: Text(_uploading ? AppLocalizations.of(context)!.uploadingText : AppLocalizations.of(context)!.uploadGiftCardButtonText),
                onPressed: _uploading ? null : _mockUpload,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
