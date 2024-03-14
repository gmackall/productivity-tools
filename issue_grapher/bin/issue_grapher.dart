import 'dart:io';
import "package:path/path.dart" show dirname, join;

import 'package:args/args.dart';

const String version = '0.0.1';

ArgParser buildParser() {
  return ArgParser()
    ..addFlag(
      'help',
      abbr: 'h',
      negatable: false,
      help: 'Print this usage information.',
    )
    ..addFlag(
      'verbose',
      abbr: 'v',
      negatable: false,
      help: 'Show additional command output.',
    )
    ..addFlag(
      'version',
      negatable: false,
      help: 'Print the tool version.',
    )
    ..addOption(
      'issue',
      help: 'The issue number (required).',
      mandatory: true
    );
}

void printUsage(ArgParser argParser) {
  print('Usage: dart issue_grapher.dart <flags> [arguments]');
  print(argParser.usage);
}

void main(List<String> arguments) {
  final ArgParser argParser = buildParser();
  try {
    final ArgResults results = argParser.parse(arguments);
    bool verbose = false;

    // Process the parsed arguments.
    if (results.wasParsed('help')) {
      printUsage(argParser);
      return;
    }
    if (results.wasParsed('issue')) {
      print('blah ${results['issue']}');
    } else {
      throw ArgumentError('Missing required argument --issue.');
    }
    if (results.wasParsed('version')) {
      print('issue_grapher version: $version');
      return;
    }
    if (results.wasParsed('verbose')) {
      verbose = true;
    }

    // Act on the arguments provided.
    print('Positional arguments: ${results.rest}');
    if (verbose) {
      print('[VERBOSE] All arguments: ${results.arguments}');
    }
    
    ProcessResult jsonData = Process.runSync(
        'gh',
        [
          'api',
          '/repos/flutter/flutter/issues/${results['issue']}/reactions',
        ]
    );
    if (jsonData.exitCode != 0) {
      print('gh api call failed. Did you make sure to run gh auth login?\n'
          'Exit code was: ${jsonData.exitCode}.\n'
          'Stderr: ${jsonData.stderr}');
    }
    // TODO this is gross
    Directory logDir = Directory('${dirname(Platform.script.path)}/../logs/')
      ..createSync(recursive: true);
    File logFile = File('${logDir.path}${results['issue']}.json');
    print('Writing gh reply data to $logFile');
    logFile.writeAsStringSync(jsonData.stdout);
  } on FormatException catch (e) {
    // Print usage information if an invalid argument was provided.
    print(e.message);
    print('');
    printUsage(argParser);
  }
}
