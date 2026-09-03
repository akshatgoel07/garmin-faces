import Toybox.Graphics;
import Toybox.Lang;
import Toybox.System;
import Toybox.Time;
import Toybox.Time.Gregorian;
import Toybox.WatchUi;

class DuoBoldView extends WatchUi.WatchFace {
    private const HOURS_Y = 114;
    private const MINUTES_Y = 291;
    private const DATE_Y = 419;
    private const JUSTIFY = Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER;

    private var _bold as FontResource?;
    private var _thin as FontResource?;
    private var _date as FontResource?;
    private var _lowPower as Boolean = false;

    function initialize() {
        WatchFace.initialize();
    }

    function onLayout(dc as Dc) as Void {
        _bold = WatchUi.loadResource(Rez.Fonts.digits_bold) as FontResource;
        _thin = WatchUi.loadResource(Rez.Fonts.digits_thin) as FontResource;
        _date = WatchUi.loadResource(Rez.Fonts.date) as FontResource;
    }

    function onUpdate(dc as Dc) as Void {
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_BLACK);
        dc.clear();

        var clock = System.getClockTime();
        var hour = clock.hour;
        if (!System.getDeviceSettings().is24Hour) {
            hour = hour % 12;
            if (hour == 0) {
                hour = 12;
            }
        }
        var hh = hour.format("%02d");
        var mm = clock.min.format("%02d");
        var cx = dc.getWidth() / 2;

        if (_lowPower) {
            // shift the thin digits a few pixels each minute so no pixel stays lit
            var dx = (clock.min % 4 < 2) ? 0 : 3;
            var dy = (clock.min % 2 == 0) ? 0 : 3;
            dc.drawText(cx + dx, HOURS_Y + dy, _thin, hh, JUSTIFY);
            dc.drawText(cx + dx, MINUTES_Y + dy, _thin, mm, JUSTIFY);
            return;
        }

        dc.drawText(cx, HOURS_Y, _bold, hh, JUSTIFY);
        dc.drawText(cx, MINUTES_Y, _bold, mm, JUSTIFY);

        var info = Gregorian.info(Time.now(), Time.FORMAT_MEDIUM);
        var label = (info.day_of_week as String).toUpper() + " " + info.day.format("%d");
        dc.drawText(cx, DATE_Y, _date, label, JUSTIFY);
    }

    function onEnterSleep() as Void {
        _lowPower = true;
        WatchUi.requestUpdate();
    }

    function onExitSleep() as Void {
        _lowPower = false;
        WatchUi.requestUpdate();
    }
}
