program seqTest
option +r;  /* reentrant: variables stored on heap */

double ctrl;
assign ctrl to "TEST:Control";
monitor ctrl;

double stateOut;
assign stateOut to "TEST:State";

ss seqMain {

    state idle {
        entry {
            stateOut = 0.0;
            pvPut(stateOut);
        }
        when (ctrl >= 1.0) {
        } state running
    }

    state running {
        entry {
            stateOut = 1.0;
            pvPut(stateOut);
        }
        when (ctrl < 1.0) {
        } state idle
    }
}
