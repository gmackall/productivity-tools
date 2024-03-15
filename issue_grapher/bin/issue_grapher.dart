import 'dart:io';
import "package:path/path.dart" show dirname;

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

    // Process the parsed arguments.
    if (results.wasParsed('help')) {
      printUsage(argParser);
      return;
    }
    if (results.wasParsed('issue')) {
      print('Processing issue number ${results['issue']}');
    } else {
      throw ArgumentError('Missing required argument --issue.');
    }
    
    ProcessResult jsonData = Process.runSync(
        'gh',
        [
          'api',
          '/repos/flutter/flutter/issues/${results['issue']}/reactions',
          '--paginate'
        ]
    );
    if (jsonData.exitCode != 0) {
      print('gh api call failed. Did you make sure to run gh auth login?\n'
          'Exit code was: ${jsonData.exitCode}.\n'
          'Stderr: ${jsonData.stderr}');
      exit(1);
    }
    // TODO this is gross
    Directory logDir = Directory('${dirname(Platform.script.path)}/../logs/')
      ..createSync(recursive: true);
    File logFile = File('${logDir.path}${results['issue']}.json');

    print('Writing gh reply data to $logFile');
    logFile.writeAsStringSync(jsonData.stdout);

    print('Creating output directory.');
    Directory('${dirname(Platform.script.path)}/../outputs/').createSync();

    print('Calling python script to generate graph.');
    ProcessResult pythonResult = Process.runSync(
        'python3',
        [
          '${dirname(Platform.script.path)}/../python/graph_results.py',
          '--issue=${results['issue']}',
        ]);
    print(pythonResult.stderr);
  } on FormatException catch (e) {
    // Print usage information if an invalid argument was provided.
    print(e.message);
    print('');
    printUsage(argParser);
  }
}
