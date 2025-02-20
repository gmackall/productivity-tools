# dependabot_app

This is a dummy flutter app which manually mirrors the dependencies used by the Flutter engine in https://github.com/flutter/flutter/blob/master/engine/src/flutter/tools/androidx/files.json. The purpose is simply to subscribe to dependabot updates in a way that gives me push notifications, as otherwise those dependencies tend to go without updates.

Do not land the dependabot PRs without first landing PRs to update the versions used by the Flutter engine.
