#
#  Copyright (c) 2018 - Present  Jeong Han Lee
#  Copyright (c) 2017 - Present  European Spallation Source ERIC
#
#  The program is free software: you can redistribute
#  it and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, either version 2 of the
#  License, or any newer version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  this program. If not, see https://www.gnu.org/licenses/gpl-2.0.txt
#
# Author  : Jeong Han Lee
# email   : han.lee@esss.se
# Date    : Saturday, February 10 18:40:25 CET 2018
# version : 

# Get where_am_I before include driver.makefile.
# After driver.makefile, where_am_I is the epics base,
# so we cannot use it


where_am_I := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

include $(E3_REQUIRE_TOOLS)/driver.makefile

SEQUENCER      :=src
SEQUENCERDEV   :=$(SEQUENCER)/dev
SEQUENCERLEMON :=$(SEQUENCER)/lemon
SEQUENCERPV    :=$(SEQUENCER)/pv
SEQUENCERSEQ   :=$(SEQUENCER)/seq
SEQUENCERSNC   :=$(SEQUENCER)/snc


USR_INCLUDES += -I$(COMMON_DIR)
USR_INCLUDES += -I$(where_am_I)/$(SEQUENCERCOMMON)
USR_INCLUDES += -I$(where_am_I)/$(SEQUENCERPV)
USR_INCLUDES += -I$(where_am_I)/$(SEQUENCERSEQUENCER)
USR_INCLUDES += -I$(where_am_I)/$(SEQUENCERSNC)


# LIBVERSION is defined in configure/CONFIG
# is transfered via Makefile
# 
SEQ_VER=$(LIBVERSION)


DBDS     = $(SEQUENCERDEV)/devSequencer.dbd

HEADERS += $(SEQUENCERPV)/pv.h
HEADERS += $(SEQUENCERPV)/pvAlarm.h
HEADERS += $(SEQUENCERPV)/pvType.h

HEADERS += $(SEQUENCERSEQ)/seqCom.h
HEADERS += $(SEQUENCERSEQ)/seqStats.h
HEADERS += $(COMMON_DIR)/seq_release.h


SOURCES += $(SEQUENCERSEQ)/seq_main.c
SOURCES += $(SEQUENCERSEQ)/seq_task.c
SOURCES += $(SEQUENCERSEQ)/seq_ca.c
SOURCES += $(SEQUENCERSEQ)/seq_if.c
SOURCES += $(SEQUENCERSEQ)/seq_mac.c
SOURCES += $(SEQUENCERSEQ)/seq_prog.c
SOURCES += $(SEQUENCERSEQ)/seq_qry.c
SOURCES += $(SEQUENCERSEQ)/seq_cmd.c
SOURCES += $(SEQUENCERSEQ)/seq_queue.c

SOURCES += $(SEQUENCERPV)/pv.cc
SOURCES += $(SEQUENCERPV)/pvNew.cc
SOURCES += $(SEQUENCERPV)/pvCa.cc

SOURCES += $(SEQUENCERDEV)/devSequencer.c


# Why!!!!

TEMP_PATH :=$(where_am_I)O.$(EPICSVERSION)_$(T_A)
LEMON     :=$(TEMP_PATH)/bin/lemon
SNC       :=$(TEMP_PATH)/bin/snc
LEMON_HOST:=$(where_am_I)O.$(EPICSVERSION)_$(EPICS_HOST_ARCH)/bin/lemon

# We are not using the snc while compiling E3 modules (no test, 
SNC_HOST:=$(where_am_I)O.$(EPICSVERSION)_$(EPICS_HOST_ARCH)/bin/snc


BINS += $(LEMON)
BINS += $(SNC)


USR_CPPFLAGS += -DPVCA


vpath %.c   $(where_am_I)$(SEQUENCERSNC)
vpath %.h   $(where_am_I)$(SEQUENCERSNC)

vpath %.lem $(where_am_I)$(SEQUENCERSNC)
vpath %.lt  $(where_am_I)$(SEQUENCERSNC)
vpath %.re  $(where_am_I)$(SEQUENCERSNC)


devSequencer$(DEP): $(COMMON_DIR)/seq_release.h $(SNC)
	@echo  $(HOSTEXE)

$(COMMON_DIR)/seq_release.h:
#	@echo "$(COMMON_DIR) O.${EPICSVERSION}_$(T_A)"
	$(RM) $@
	$(PERL) $(where_am_I)$(SEQUENCERSEQ)/seq_release.pl $(SEQ_VER) > $@


# We only use linux, so I added $(OP_SYS_LDFLAGS) $(ARCH_DEP_LDFLAGS)
$(SNC): lexer.c $(patsubst %.c,%.o, lexer.c snl.c main.c expr.c var_types.c analysis.c gen_code.c gen_ss_code.c gen_tables.c builtin.c  sym_table.c )
	@echo ""
	@echo ">>>>> snc Init "
	$(CCC) -o $@ -L $(EPICS_BASE_LIB) -Wl,-rpath,$(EPICS_BASE_LIB) $(OP_SYS_LDFLAGS) $(ARCH_DEP_LDFLAGS)  $(filter %.o, $^) -lCom -ldbRecStd -ldbCore -lca 
	@echo "<<<<< snc Done"
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
	@echo ">>>>> lemon Init "
	$(RM) $@
	$(MKDIR) -p $(TEMP_PATH)/bin
	$(COMPILE.c) -o $(LEMON) $(OP_SYS_CFLAGS) $(ARCH_DEP_CFLAGS) $^
	@echo "<<<<< lemon Done "
	@echo ""


db:
#
.PHONY: vlibs
vlibs:
#
