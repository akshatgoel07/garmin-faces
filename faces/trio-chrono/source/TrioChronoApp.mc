import Toybox.Application;
import Toybox.Lang;
import Toybox.WatchUi;

class TrioChronoApp extends Application.AppBase {
    private var _view as TrioChronoView?;

    function initialize() {
        AppBase.initialize();
    }

    function getInitialView() as [Views] or [Views, InputDelegates] {
        _view = new TrioChronoView();
        return [_view];
    }

    function onSettingsChanged() as Void {
        if (_view != null) {
            _view.loadTheme();
        }
        WatchUi.requestUpdate();
    }
}
