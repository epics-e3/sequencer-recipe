#
# LEGACY_RSET should be defined before driver.makefile
# require-ess from 3.0.1
#LEGACY_RSET = YES

where_am_I := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(E3_REQUIRE_TOOLS)/driver.makefile

USR_CPPFLAGS += -DUSE_TYPED_RSET


# LIBVERSION is defined in configure/CONFIG
# is transfered via Makefile
# 
SEQ_VER=$(LIBVERSION)


SEQUENCER      :=src
SEQUENCERPV    :=$(SEQUENCER)/pv
SEQUENCERCOMMON:=$(SEQUENCER)/common
SEQUENCERSEQ   :=$(SEQUENCER)/seq
SEQUENCERLEMON :=$(SEQUENCER)/lemon
SEQUENCERSNC   :=$(SEQUENCER)/snc


USR_INCLUDES += -I$(COMMON_DIR)
USR_INCLUDES += -I$(where_am_I)$(SEQUENCERPV)
USR_INCLUDES += -I$(where_am_I)$(SEQUENCERCOMMON)
USR_INCLUDES += -I$(where_am_I)$(SEQUENCERSEQ)
USR_INCLUDES += -I$(where_am_I)$(SEQUENCERSNC)


HEADERS += $(SEQUENCERSEQ)/seqCom.h
HEADERS += $(SEQUENCERSEQ)/seqStats.h
HEADERS += $(SEQUENCERSEQ)/seq_snc.h


SOURCES += $(SEQUENCERSEQ)/seq_main.c
SOURCES += $(SEQUENCERSEQ)/seq_task.c
SOURCES += $(SEQUENCERSEQ)/seq_ca.c
SOURCES += $(SEQUENCERSEQ)/seq_if.c
SOURCES += $(SEQUENCERSEQ)/seq_mac.c
SOURCES += $(SEQUENCERSEQ)/seq_prog.c
SOURCES += $(SEQUENCERSEQ)/seq_qry.c
SOURCES += $(SEQUENCERSEQ)/seq_cmd.c
SOURCES += $(SEQUENCERSEQ)/seq_queue.c


HEADERS += $(SEQUENCERCOMMON)/seq_mask.h
HEADERS += $(SEQUENCERCOMMON)/seq_prim_types.h
HEADERS += $(COMMON_DIR)/seq_release.h


HEADERS += $(SEQUENCERPV)/pv.h
HEADERS += $(SEQUENCERPV)/pvAlarm.h
HEADERS += $(SEQUENCERPV)/pvType.h

SOURCES += $(SEQUENCERPV)/pv.c

HEADERS += $(SEQUENCERSNC)/seqMain.c


TEMP_PATH :=$(where_am_I)O.$(EPICSVERSION)_$(T_A)
LEMON     :=$(TEMP_PATH)/bin/lemon
SNC       :=$(TEMP_PATH)/bin/snc
LEMON_HOST:=$(where_am_I)O.$(EPICSVERSION)_$(EPICS_HOST_ARCH)/bin/lemon

# We are not using the snc while compiling E3 modules (no test, 
SNC_HOST:=$(where_am_I)O.$(EPICSVERSION)_$(EPICS_HOST_ARCH)/bin/snc

# Note that lemon only need to be built for the host architecture.
BINS += $(LEMON)
BINS += $(SNC)


vpath %.c   $(where_am_I)$(SEQUENCERSNC)
vpath %.h   $(where_am_I)$(SEQUENCERSNC)

vpath %.lem $(where_am_I)$(SEQUENCERSNC)
vpath %.lt  $(where_am_I)$(SEQUENCERSNC)
vpath %.re  $(where_am_I)$(SEQUENCERSNC)


pv$(DEP): $(COMMON_DIR)/seq_release.h

$(COMMON_DIR)/seq_release.h:
	$(RM) $@
	$(PERL) $(where_am_I)$(SEQUENCERCOMMON)/seq_release.pl $(SEQ_VER) > $@


$(DEPFILE): $(SNC)

# We only use linux, so I added $(OP_SYS_LDFLAGS) $(ARCH_DEP_LDFLAGS)
$(SNC): lexer.c $(patsubst %.c,%.o, lexer.c snl.c main.c node.c var_types.c analysis.c gen_code.c gen_ss_code.c gen_tables.c sym_table.c builtin.c type_check.c )
	@echo ""
	@echo ""
	@echo ">>>>> snc Init "
	$(CCC) -o $@ -L $(EPICS_BASE_LIB) -Wl,-rpath,$(EPICS_BASE_LIB) $(OP_SYS_LDFLAGS) $(ARCH_DEP_LDFLAGS)  $(filter %.o, $^) -lCom
	@echo "<<<<< snc Done"
	@echo ""
	@echo ""

lexer.c: snl.re snl.h
	re2c -s -b -o $@ $<

snl.c snl.h: $(addprefix $(where_am_I)$(SEQUENCERSNC)/, snl.lem snl.lt) $(LEMON)
	$(RM) snl.c snl.h
	$(LEMON_HOST) o=. $<



# 
# lemon is called in the host, so the hard-coded gcc, which is the host
# If one changes it to $(COMPILE.c), the compiling process fails.
# driver.makefile is trying to find the binary in $(where_am_I)
# not in O.3.15.5_linux-x86_64. So I copy it to $(where_am_I)
# OR we have to remove ../ prefix in driver.makefile as 
# ${INSTALL_BINS}: $(addprefix ../,$(filter-out /%,${BINS})) $(filter /%,${BINS})
#	@echo "Installing binaries $^ to $(@D)"
#	$(INSTALL) -d -m555 $^ $(@D)
#
#
#
# $(LINK.c) doesn't work, because it use driver.makefile instead of EPICS BASE
#
$(LEMON): $(where_am_I)$(SEQUENCERLEMON)/lemon.c
	@echo ""
	@echo ""
	@echo ">>>>> lemon Init "
	$(RM) $@
	$(MKDIR) -p $(TEMP_PATH)/bin
	$(COMPILE.c) -o $(LEMON) $(OP_SYS_CFLAGS) $(ARCH_DEP_CFLAGS) $^
	@echo "<<<<< lemon Done "
	@echo ""
	@echo ""


.PHONY:
.PHONY: vlibs
vlibs:
